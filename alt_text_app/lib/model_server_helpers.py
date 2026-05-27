"""
Helper functions for model-server API integration.

Called by:
    - alt_text_app.lib.sync_processing_helpers (synchronous attempts)
    - scripts.process_alt_text_generation (cron background processing)
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import httpx
from django.conf import settings as project_settings
from django.utils import timezone as django_timezone

from alt_text_app.models import GeneratedAltText

log = logging.getLogger(__name__)

PROMPT_FILE_PATH = Path(__file__).resolve().parent / 'prompt.md'


@dataclass(frozen=True)
class ModelServerConfig:
    """
    Holds settings for the selected OpenAI-compatible model server.
    """

    server: str
    base_url: str
    api_key: str
    model_order: list[str]
    extra_headers: dict[str, str]


def load_prompt_template() -> str:
    """
    Loads the alt-text prompt template from disk.
    """
    prompt_text = PROMPT_FILE_PATH.read_text(encoding='utf-8')
    return prompt_text


def build_prompt() -> str:
    """
    Builds the prompt for alt-text generation.
    """
    prompt = load_prompt_template()
    log.debug(f'prompt, ``{prompt}``')
    return prompt


def get_model_server_config() -> ModelServerConfig:
    """
    Builds configuration for the selected model server.
    """
    server = project_settings.MODEL_SERVER

    if server == 'openrouter':
        config = ModelServerConfig(
            server=server,
            base_url=project_settings.OPENROUTER_BASE_URL,
            api_key=project_settings.OPENROUTER_API_KEY,
            model_order=list(project_settings.OPENROUTER_MODEL_ORDER),
            extra_headers={
                'HTTP-Referer': 'https://library.brown.edu',
                'X-Title': 'Image Alt Text Maker',
            },
        )
    elif server == 'lmstudio':
        config = ModelServerConfig(
            server=server,
            base_url=project_settings.LMSTUDIO_BASE_URL,
            api_key=project_settings.LMSTUDIO_API_KEY,
            model_order=list(project_settings.LMSTUDIO_MODEL_ORDER),
            extra_headers={},
        )
    else:
        raise ValueError(f'Unsupported MODEL_SERVER: {server}')

    return config


def validate_model_server_config(config: ModelServerConfig) -> None:
    """
    Validates that the selected model server has the required settings.
    """
    if not config.base_url:
        raise ValueError(f'{config.server} base URL is not configured')
    if not config.api_key:
        raise ValueError(f'{config.server} API key is not configured')
    if not config.model_order:
        raise ValueError(f'{config.server} model order is not configured')


def get_headers(config: ModelServerConfig) -> dict[str, str]:
    """
    Builds request headers for the selected model server.
    """
    headers = {
        'Authorization': f'Bearer {config.api_key}',
        'Content-Type': 'application/json',
    }
    headers.update(config.extra_headers)
    return headers


def get_chat_completions_url(config: ModelServerConfig) -> str:
    """
    Builds the OpenAI-compatible chat completions URL.
    """
    url = f'{config.base_url.rstrip("/")}/chat/completions'
    return url


def build_chat_completion_payload(prompt: str, model: str, image_data_url: str) -> dict[str, object]:
    """
    Builds the OpenAI-compatible chat completion payload.
    """
    payload: dict[str, object] = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    {'type': 'image_url', 'image_url': {'url': image_data_url}},
                ],
            }
        ],
    }
    return payload


def call_model_server(
    prompt: str,
    config: ModelServerConfig,
    model: str,
    timeout_seconds: float,
    image_data_url: str,
) -> dict:
    """
    Calls the selected model server with the given prompt.
    Returns the raw response JSON.

    Raises:
        httpx.TimeoutException: If the request exceeds timeout_seconds.
        httpx.HTTPStatusError: If the API returns an error status.

    Note: Only one of our servers requires a non-default certificate to be specified,
          so the SYSTEM_CA_BUNDLE environment variable is implemented optionally.
    """
    validate_model_server_config(config)
    headers = get_headers(config)
    payload = build_chat_completion_payload(prompt, model, image_data_url)
    url = get_chat_completions_url(config)

    client_kwargs = {'timeout': timeout_seconds}
    system_ca_bundle = project_settings.SYSTEM_CA_BUNDLE
    if system_ca_bundle:
        client_kwargs['verify'] = system_ca_bundle

    with httpx.Client(**client_kwargs) as client:
        response = client.post(url, headers=headers, json=payload)
        log.debug(f'response, ``{response}``')
        if response.is_error:
            log.error(
                'Model-server request failed with status=%s, server=%s, model=%s, response=%s',
                response.status_code,
                config.server,
                model,
                response.text,
            )
        response.raise_for_status()
        jsn_response = response.json()
        log.debug(f'jsn_response, ``{jsn_response}``')

    return jsn_response


def call_model_server_with_model_order(
    prompt: str,
    config: ModelServerConfig,
    timeout_seconds: float,
    image_data_url: str,
) -> dict:
    """
    Calls the selected model server with models in the provided order until one succeeds.
    """
    validate_model_server_config(config)
    last_exception: Exception | None = None
    response_json: dict = {}
    log.debug('Model-server order for %s: %s', config.server, config.model_order)

    for index, model in enumerate(config.model_order, start=1):
        try:
            log.info(
                'Model-server attempt %s/%s with server=%s, model=%s',
                index,
                len(config.model_order),
                config.server,
                model,
            )
            response_json = call_model_server(prompt, config, model, timeout_seconds, image_data_url)
            last_exception = None
            break
        except Exception as exc:
            last_exception = exc
            log.warning('Model-server call failed for server=%s, model=%s, trying next if available', config.server, model)

    if last_exception is not None:
        raise last_exception

    return response_json


def parse_model_server_response(response_json: dict, config: ModelServerConfig) -> dict:
    """
    Parses the model-server response and extracts relevant fields.
    """
    result = {
        'alt_text': '',
        'response_id': response_json.get('id', ''),
        'model_server': config.server,
        'base_url': config.base_url,
        'provider': response_json.get('provider', ''),
        'model': response_json.get('model', ''),
        'finish_reason': '',
        'response_created_at': None,
        'prompt_tokens': None,
        'completion_tokens': None,
        'total_tokens': None,
    }

    ## Extract alt text from choices
    choices = response_json.get('choices', [])
    if choices:
        choice = choices[0]
        message = choice.get('message', {})
        content = message.get('content', '')
        if isinstance(content, list):
            content_text_items = [
                item.get('text', '') for item in content if isinstance(item, dict) and item.get('type') == 'text'
            ]
            result['alt_text'] = '\n'.join([text for text in content_text_items if text]).strip()
        else:
            result['alt_text'] = str(content).strip()
        result['finish_reason'] = choice.get('finish_reason', '')

    ## Extract usage info
    usage = response_json.get('usage', {})
    result['prompt_tokens'] = usage.get('prompt_tokens')
    result['completion_tokens'] = usage.get('completion_tokens')
    result['total_tokens'] = usage.get('total_tokens')

    ## Extract created timestamp
    created = response_json.get('created')
    if created:
        utc_dt = datetime.fromtimestamp(created, tz=timezone.utc)
        result['response_created_at'] = django_timezone.make_naive(utc_dt)

    return result


def persist_generated_alt_text(alt_text_record: GeneratedAltText, response_json: dict, parsed: dict) -> None:
    """
    Persists the model-server response to the alt-text model instance.
    """
    alt_text_record.raw_response_json = response_json
    alt_text_record.alt_text = parsed['alt_text']
    alt_text_record.response_id = parsed['response_id']
    alt_text_record.model_server = parsed['model_server']
    alt_text_record.base_url = parsed['base_url']
    alt_text_record.provider = parsed['provider']
    alt_text_record.model = parsed['model']
    alt_text_record.finish_reason = parsed['finish_reason']
    alt_text_record.response_created_at = parsed['response_created_at']
    alt_text_record.prompt_tokens = parsed['prompt_tokens']
    alt_text_record.completion_tokens = parsed['completion_tokens']
    alt_text_record.total_tokens = parsed['total_tokens']
    utc_now = datetime.now(tz=timezone.utc)
    naive_now = django_timezone.make_naive(utc_now)
    alt_text_record.status = 'completed'
    alt_text_record.completed_at = naive_now
    alt_text_record.error = None
    alt_text_record.save()
