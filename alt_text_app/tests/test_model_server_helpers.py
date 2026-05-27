"""
Tests for model-server helper functions.
"""

from django.test import TestCase
from django.test.utils import override_settings

from alt_text_app.lib import model_server_helpers


class ModelServerConfigTest(TestCase):
    """
    Checks model-server configuration helpers.
    """

    @override_settings(
        MODEL_SERVER='openrouter',
        OPENROUTER_BASE_URL='https://openrouter.ai/api/v1',
        OPENROUTER_API_KEY='openrouter-key',
        OPENROUTER_MODEL_ORDER=['openrouter/model-one', 'openrouter/model-two'],
    )
    def test_openrouter_config(self) -> None:
        """
        Checks that OpenRouter settings build the expected config and headers.
        """
        config = model_server_helpers.get_model_server_config()
        headers = model_server_helpers.get_headers(config)
        url = model_server_helpers.get_chat_completions_url(config)

        self.assertEqual(config.server, 'openrouter')
        self.assertEqual(config.base_url, 'https://openrouter.ai/api/v1')
        self.assertEqual(config.model_order, ['openrouter/model-one', 'openrouter/model-two'])
        self.assertEqual(url, 'https://openrouter.ai/api/v1/chat/completions')
        self.assertEqual(headers['Authorization'], 'Bearer openrouter-key')
        self.assertEqual(headers['HTTP-Referer'], 'https://library.brown.edu')
        self.assertEqual(headers['X-Title'], 'Image Alt Text Maker')

    @override_settings(
        MODEL_SERVER='lmstudio',
        LMSTUDIO_BASE_URL='http://127.0.0.1:1234/v1',
        LMSTUDIO_API_KEY='lm-studio',
        LMSTUDIO_MODEL_ORDER=['local-model-one', 'local-model-two'],
    )
    def test_lmstudio_config(self) -> None:
        """
        Checks that LM Studio settings build the expected config and headers.
        """
        config = model_server_helpers.get_model_server_config()
        headers = model_server_helpers.get_headers(config)
        url = model_server_helpers.get_chat_completions_url(config)

        self.assertEqual(config.server, 'lmstudio')
        self.assertEqual(config.base_url, 'http://127.0.0.1:1234/v1')
        self.assertEqual(config.model_order, ['local-model-one', 'local-model-two'])
        self.assertEqual(url, 'http://127.0.0.1:1234/v1/chat/completions')
        self.assertEqual(headers['Authorization'], 'Bearer lm-studio')
        self.assertNotIn('HTTP-Referer', headers)
        self.assertNotIn('X-Title', headers)

    def test_build_chat_completion_payload(self) -> None:
        """
        Checks that the payload uses an OpenAI-compatible multimodal image_url shape.
        """
        payload = model_server_helpers.build_chat_completion_payload(
            'Describe this image.',
            'test-model',
            'data:image/png;base64,abc123',
        )

        self.assertEqual(payload['model'], 'test-model')
        messages = payload['messages']
        self.assertIsInstance(messages, list)
        content = messages[0]['content']
        self.assertEqual(content[0], {'type': 'text', 'text': 'Describe this image.'})
        self.assertEqual(content[1], {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,abc123'}})

    def test_validate_missing_settings(self) -> None:
        """
        Checks that missing selected-provider settings fail clearly.
        """
        config = model_server_helpers.ModelServerConfig(
            server='openrouter',
            base_url='',
            api_key='',
            model_order=[],
            extra_headers={},
        )

        with self.assertRaises(ValueError) as context:
            model_server_helpers.validate_model_server_config(config)

        self.assertIn('base URL', str(context.exception))

    @override_settings(
        MODEL_SERVER='openrouter',
        OPENROUTER_BASE_URL='https://openrouter.ai/api/v1',
        OPENROUTER_API_KEY='openrouter-key',
        OPENROUTER_MODEL_ORDER=['openrouter/model-one'],
    )
    def test_parse_model_server_response(self) -> None:
        """
        Checks that a standard OpenAI-compatible response is parsed.
        """
        config = model_server_helpers.get_model_server_config()
        response_json = {
            'id': 'response-id',
            'provider': 'provider-name',
            'model': 'model-name',
            'choices': [{'message': {'content': 'A clear alt text.'}, 'finish_reason': 'stop'}],
            'usage': {'prompt_tokens': 1, 'completion_tokens': 2, 'total_tokens': 3},
            'created': 1234567890,
        }

        parsed = model_server_helpers.parse_model_server_response(response_json, config)

        self.assertEqual(parsed['alt_text'], 'A clear alt text.')
        self.assertEqual(parsed['response_id'], 'response-id')
        self.assertEqual(parsed['model_server'], 'openrouter')
        self.assertEqual(parsed['base_url'], 'https://openrouter.ai/api/v1')
        self.assertEqual(parsed['provider'], 'provider-name')
        self.assertEqual(parsed['model'], 'model-name')
        self.assertEqual(parsed['finish_reason'], 'stop')
        self.assertEqual(parsed['prompt_tokens'], 1)
        self.assertEqual(parsed['completion_tokens'], 2)
        self.assertEqual(parsed['total_tokens'], 3)
        self.assertIsNotNone(parsed['response_created_at'])
