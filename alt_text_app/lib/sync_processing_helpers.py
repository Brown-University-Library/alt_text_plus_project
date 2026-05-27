"""
Synchronous image processing helpers with timeout fallback.
Handles model-server processing attempts with graceful degradation.

Called by:
    - alt_text_app.views.upload_image()
"""

import datetime
import logging
from pathlib import Path

import httpx
from django.conf import settings as project_settings
from django.utils import timezone as django_timezone

from alt_text_app.lib import image_helpers, model_server_helpers
from alt_text_app.models import GeneratedAltText, ImageDocument

log = logging.getLogger(__name__)


def attempt_synchronous_processing(doc: ImageDocument, image_path: Path) -> None:
    """
    Attempts to run alt-text generation synchronously with timeouts.
    Updates doc status in-place. Falls back to 'pending' on timeout.
    """
    log.debug(f'starting attempt_synchronous_processing() for document ``{doc.pk}')
    ## Mark as processing and set timestamp
    doc.processing_status = 'processing'
    doc.processing_error = None
    doc.processing_started_at = datetime.datetime.now()
    doc.save(update_fields=['processing_status', 'processing_error', 'processing_started_at'])
    try:
        attempt_alt_text_sync(doc, image_path)
    except Exception as exc:
        log.exception('Alt-text generation failed for document %s', doc.pk)
        doc.processing_status = 'failed'
        doc.processing_error = str(exc)
        doc.save(update_fields=['processing_status', 'processing_error'])


def attempt_alt_text_sync(doc: ImageDocument, image_path: Path) -> bool:
    """
    Attempts synchronous alt-text generation with timeout.
    Returns True if successful, False if timeout or error.
    """
    log.debug(f'starting attempt_alt_text_sync() for document ``{doc.pk}')
    config = model_server_helpers.get_model_server_config()

    try:
        model_server_helpers.validate_model_server_config(config)
    except ValueError as exc:
        log.warning('Model-server settings not available, skipping sync attempt for document %s: %s', doc.pk, exc)
        return False

    timeout_seconds = project_settings.MODEL_SYNC_TIMEOUT_SECONDS

    ## Create alt-text record with 'processing' status BEFORE calling API
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc)
    naive_now = django_timezone.make_naive(utc_now)
    alt_text_record, created = GeneratedAltText.objects.get_or_create(
        image_document=doc,
        defaults={
            'status': 'processing',
            'requested_at': naive_now,
            'model_server': config.server,
            'base_url': config.base_url,
        },
    )

    if not created:
        alt_text_record.status = 'processing'
        alt_text_record.requested_at = naive_now
        alt_text_record.error = None
        alt_text_record.model_server = config.server
        alt_text_record.base_url = config.base_url
        alt_text_record.save(update_fields=['status', 'requested_at', 'error', 'model_server', 'base_url'])

    try:
        log.info('Attempting synchronous alt-text generation for document %s with server=%s', doc.pk, config.server)

        prompt = model_server_helpers.build_prompt()

        ## Save prompt
        alt_text_record.prompt = prompt
        alt_text_record.save(update_fields=['prompt'])

        image_data_url = image_helpers.build_image_data_url(image_path, doc.mime_type)

        ## Call API with timeout
        response_json = model_server_helpers.call_model_server_with_model_order(
            prompt,
            config,
            timeout_seconds,
            image_data_url,
        )
        parsed = model_server_helpers.parse_model_server_response(response_json, config)

        ## Persist
        model_server_helpers.persist_generated_alt_text(alt_text_record, response_json, parsed)
        doc.processing_status = 'completed'
        doc.processing_error = None
        doc.save(update_fields=['processing_status', 'processing_error'])
        log.info('Synchronous alt-text generation succeeded for document %s with server=%s', doc.pk, config.server)
        return True

    except httpx.TimeoutException:
        log.warning('Model-server timed out for document %s, falling back to cron', doc.pk)
        alt_text_record.status = 'pending'
        alt_text_record.error = 'Sync attempt timed out; will retry in background.'
        alt_text_record.save(update_fields=['status', 'error'])
        doc.processing_status = 'pending'
        doc.processing_started_at = None
        doc.save(update_fields=['processing_status', 'processing_started_at'])
        return False

    except Exception as exc:
        log.exception('Alt-text generation failed for document %s', doc.pk)
        alt_text_record.status = 'failed'
        alt_text_record.error = str(exc)
        alt_text_record.save(update_fields=['status', 'error'])
        doc.processing_status = 'failed'
        doc.processing_error = str(exc)
        doc.save(update_fields=['processing_status', 'processing_error'])
        return False
