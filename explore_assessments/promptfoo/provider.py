"""
Promptfoo provider for repo-local alt-text assessment runs.

The provider calls the same OpenAI-compatible model-server path used by the
Django app, but it does not create ImageDocument or GeneratedAltText records.
"""

from __future__ import annotations

import mimetypes
import os
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_TIMEOUT_SECONDS = 60.0
_DJANGO_IS_READY = False


def call_api(prompt: str, options: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """
    Promptfoo Python-provider entrypoint.

    Expected test vars:
        image_path: path relative to promptfooconfig.yaml, or absolute path
        mime_type: optional MIME type; guessed from image_path if omitted

    Useful provider config:
        model: explicit model id
        model_env_var: environment variable containing a model id
        allow_app_model_fallback: use the app's first configured model if no
            explicit/env model is supplied
        model_params: extra OpenAI-compatible chat-completion parameters
        timeout_seconds: per-request timeout
        mock_response: optional local response for provider smoke tests
    """
    provider_config = options.get('config') or {}

    mock_response = provider_config.get('mock_response')
    if mock_response is not None:
        return {
            'output': str(mock_response),
            'cached': False,
            'metadata': {
                'mock': True,
            },
        }

    try:
        return _call_model_server(prompt, provider_config, context)
    except Exception as exc:
        return {
            'output': '',
            'error': str(exc),
        }


def _call_model_server(prompt: str, provider_config: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    _setup_django()

    from django.conf import settings as project_settings

    from alt_text_app.lib import image_helpers, model_server_helpers

    app_config = model_server_helpers.get_model_server_config()
    model, model_source = _select_model(provider_config, app_config.model_order)
    request_config = replace(app_config, model_order=[model])
    model_server_helpers.validate_model_server_config(request_config)

    vars_map = context.get('vars') or {}
    image_path_value = vars_map.get('image_path')
    if not image_path_value:
        raise ValueError('Promptfoo test vars must include image_path')

    base_path = provider_config.get('basePath') or Path(__file__).resolve().parent
    image_path = _resolve_path(str(image_path_value), Path(base_path))
    if not image_path.exists():
        raise FileNotFoundError(f'Image file not found: {image_path}')

    mime_type = vars_map.get('mime_type') or mimetypes.guess_type(image_path.name)[0] or 'image/*'
    image_data_url = image_helpers.build_image_data_url(image_path, str(mime_type))

    payload = model_server_helpers.build_chat_completion_payload(prompt, model, image_data_url)
    for key, value in (provider_config.get('model_params') or {}).items():
        if key not in {'model', 'messages'}:
            payload[key] = value

    timeout_seconds = float(provider_config.get('timeout_seconds', DEFAULT_TIMEOUT_SECONDS))
    client_kwargs: dict[str, Any] = {'timeout': timeout_seconds}
    system_ca_bundle = getattr(project_settings, 'SYSTEM_CA_BUNDLE', '')
    if system_ca_bundle:
        client_kwargs['verify'] = system_ca_bundle

    started = time.monotonic()
    with httpx.Client(**client_kwargs) as client:
        response = client.post(
            model_server_helpers.get_chat_completions_url(request_config),
            headers=model_server_helpers.get_headers(request_config),
            json=payload,
        )
        if response.is_error:
            raise httpx.HTTPStatusError(
                f'Model-server request failed with status={response.status_code}: {response.text}',
                request=response.request,
                response=response,
            )
        response_json = response.json()
    latency_ms = int((time.monotonic() - started) * 1000)

    parsed = model_server_helpers.parse_model_server_response(response_json, request_config)
    usage = response_json.get('usage') or {}
    token_usage = {
        'total': usage.get('total_tokens') or 0,
        'prompt': usage.get('prompt_tokens') or 0,
        'completion': usage.get('completion_tokens') or 0,
        'numRequests': 1,
    }

    result: dict[str, Any] = {
        'output': parsed['alt_text'],
        'tokenUsage': token_usage,
        'latencyMs': latency_ms,
        'metadata': {
            'case_id': vars_map.get('case_id', ''),
            'image_path': str(image_path),
            'model_source': model_source,
            'model_server': parsed['model_server'],
            'provider': parsed['provider'],
            'model': parsed['model'] or model,
            'finish_reason': parsed['finish_reason'],
            'response_id': parsed['response_id'],
            'base_url': parsed['base_url'],
            'model_params': provider_config.get('model_params') or {},
        },
    }

    cost = _extract_cost(response_json)
    if cost is not None:
        result['cost'] = cost

    return result


def _setup_django() -> None:
    global _DJANGO_IS_READY
    if _DJANGO_IS_READY:
        return

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    import django

    django.setup()
    _DJANGO_IS_READY = True


def _select_model(provider_config: dict[str, Any], app_model_order: list[str]) -> tuple[str, str]:
    explicit_model = str(provider_config.get('model') or '').strip()
    if explicit_model:
        return explicit_model, 'provider-config:model'

    model_env_var = str(provider_config.get('model_env_var') or '').strip()
    if model_env_var:
        env_model = os.environ.get(model_env_var, '').strip()
        if env_model:
            return env_model, f'env:{model_env_var}'

    allow_app_model_fallback = bool(provider_config.get('allow_app_model_fallback', True))
    if allow_app_model_fallback and app_model_order:
        return app_model_order[0], 'app-config:model_order[0]'

    if model_env_var:
        raise ValueError(f'Model environment variable is not set: {model_env_var}')
    raise ValueError('Provider config must set model or model_env_var, or app settings must define a model order')


def _resolve_path(path_value: str, base_path: Path) -> Path:
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = base_path / path
    return path.resolve()


def _extract_cost(response_json: dict[str, Any]) -> float | None:
    usage = response_json.get('usage') or {}
    possible_cost = usage.get('cost') or usage.get('total_cost') or response_json.get('cost')
    if possible_cost is None:
        return None
    try:
        return float(possible_cost)
    except (TypeError, ValueError):
        return None
