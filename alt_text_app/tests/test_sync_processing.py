"""
Tests for synchronous image processing with timeout fallback.
"""

import logging
import tempfile
from pathlib import Path
from unittest.mock import patch

import httpx
from django.test import TestCase

from alt_text_app.lib.model_server_helpers import ModelServerConfig
from alt_text_app.lib.sync_processing_helpers import attempt_alt_text_sync
from alt_text_app.models import GeneratedAltText, ImageDocument

log = logging.getLogger(__name__)


class SyncModelServerProcessingTest(TestCase):
    """
    Checks synchronous model-server processing with timeout handling.
    """

    def setUp(self) -> None:
        """
        Creates a test document and image file.
        """
        self.doc = ImageDocument.objects.create(
            original_filename='test.png',
            file_checksum='abc123',
            file_size=1024,
            mime_type='image/png',
            file_extension='png',
            processing_status='pending',
        )
        self.temp_dir = tempfile.TemporaryDirectory()
        self.image_path = Path(self.temp_dir.name) / 'test.png'
        self.image_path.write_bytes(b'\x89PNG\r\n\x1a\n' + b'test')

    def tearDown(self) -> None:
        """
        Cleans up temporary files.
        """
        self.temp_dir.cleanup()

    def test_alt_text_sync_success(self) -> None:
        """
        Checks that successful model-server processing updates alt text to 'completed'.
        """
        mock_response = {
            'id': 'test-id',
            'provider': 'test-provider',
            'model': 'test-model',
            'choices': [{'message': {'content': 'A cat on a mat.'}, 'finish_reason': 'stop'}],
            'usage': {'prompt_tokens': 10, 'completion_tokens': 20, 'total_tokens': 30},
            'created': 1234567890,
        }
        config = ModelServerConfig(
            server='openrouter',
            base_url='https://openrouter.ai/api/v1',
            api_key='test-key',
            model_order=['test-model'],
            extra_headers={},
        )

        with patch(
            'alt_text_app.lib.sync_processing_helpers.model_server_helpers.get_model_server_config',
            return_value=config,
        ):
            with patch(
                'alt_text_app.lib.sync_processing_helpers.model_server_helpers.build_prompt',
                return_value='test prompt',
            ):
                with patch(
                    'alt_text_app.lib.sync_processing_helpers.model_server_helpers.call_model_server_with_model_order',
                    return_value=mock_response,
                ):
                    result = attempt_alt_text_sync(self.doc, self.image_path)

        self.assertTrue(result)
        self.doc.refresh_from_db()
        self.assertEqual(self.doc.processing_status, 'completed')
        alt_text_record = GeneratedAltText.objects.get(image_document=self.doc)
        self.assertEqual(alt_text_record.status, 'completed')
        self.assertEqual(alt_text_record.alt_text, 'A cat on a mat.')
        self.assertEqual(alt_text_record.model_server, 'openrouter')
        self.assertEqual(alt_text_record.base_url, 'https://openrouter.ai/api/v1')

    def test_alt_text_sync_timeout_fallback(self) -> None:
        """
        Checks that model-server timeout sets alt-text status to 'pending'.
        """
        config = ModelServerConfig(
            server='openrouter',
            base_url='https://openrouter.ai/api/v1',
            api_key='test-key',
            model_order=['test-model'],
            extra_headers={},
        )
        with patch(
            'alt_text_app.lib.sync_processing_helpers.model_server_helpers.get_model_server_config',
            return_value=config,
        ):
            with patch(
                'alt_text_app.lib.sync_processing_helpers.model_server_helpers.build_prompt',
                return_value='test prompt',
            ):
                with patch(
                    'alt_text_app.lib.sync_processing_helpers.model_server_helpers.call_model_server_with_model_order',
                    side_effect=httpx.TimeoutException('timeout'),
                ):
                    result = attempt_alt_text_sync(self.doc, self.image_path)

        self.assertFalse(result)
        alt_text_record = GeneratedAltText.objects.get(image_document=self.doc)
        self.assertEqual(alt_text_record.status, 'pending')
        self.assertIn('timed out', alt_text_record.error)
        self.doc.refresh_from_db()
        self.assertEqual(self.doc.processing_status, 'pending')

    def test_alt_text_sync_error_marks_failed(self) -> None:
        """
        Checks that non-timeout errors mark alt text as 'failed'.
        """
        config = ModelServerConfig(
            server='openrouter',
            base_url='https://openrouter.ai/api/v1',
            api_key='test-key',
            model_order=['test-model'],
            extra_headers={},
        )
        with patch(
            'alt_text_app.lib.sync_processing_helpers.model_server_helpers.get_model_server_config',
            return_value=config,
        ):
            with patch(
                'alt_text_app.lib.sync_processing_helpers.model_server_helpers.build_prompt',
                return_value='test prompt',
            ):
                with patch(
                    'alt_text_app.lib.sync_processing_helpers.model_server_helpers.call_model_server_with_model_order',
                    side_effect=Exception('API error'),
                ):
                    result = attempt_alt_text_sync(self.doc, self.image_path)

        self.assertFalse(result)
        alt_text_record = GeneratedAltText.objects.get(image_document=self.doc)
        self.assertEqual(alt_text_record.status, 'failed')
        self.assertIn('API error', alt_text_record.error)
        self.doc.refresh_from_db()
        self.assertEqual(self.doc.processing_status, 'failed')

    def test_alt_text_skipped_without_credentials(self) -> None:
        """
        Checks that alt-text generation is skipped if settings are missing.
        """
        config = ModelServerConfig(
            server='openrouter',
            base_url='https://openrouter.ai/api/v1',
            api_key='',
            model_order=['test-model'],
            extra_headers={},
        )
        with patch(
            'alt_text_app.lib.sync_processing_helpers.model_server_helpers.get_model_server_config',
            return_value=config,
        ):
            result = attempt_alt_text_sync(self.doc, self.image_path)

        self.assertFalse(result)
        self.assertFalse(GeneratedAltText.objects.filter(image_document=self.doc).exists())
