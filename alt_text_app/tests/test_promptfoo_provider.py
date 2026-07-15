"""
Tests for the Promptfoo model-server provider.
"""

from unittest.mock import Mock, patch

import httpx
from django.test import SimpleTestCase

from explore_assessments.promptfoo import provider as promptfoo_provider


class PromptfooProviderRetryTest(SimpleTestCase):
    """
    Checks retry handling for temporary LM Studio failures.
    """

    def test_retries_connection_error_then_returns_response(self) -> None:
        """
        Checks that a refused connection is retried before returning a successful response.
        """
        url = 'http://127.0.0.1:1234/v1/chat/completions'
        request = httpx.Request('POST', url)
        client = Mock()
        client.post.side_effect = [
            httpx.ConnectError('Connection refused', request=request),
            httpx.Response(200, json={'choices': []}, request=request),
        ]

        with patch.object(promptfoo_provider.time, 'sleep') as sleep_mock:
            response_json, attempts = promptfoo_provider._post_chat_completion_with_retries(
                client,
                url,
                {},
                {},
                max_attempts=2,
                retry_delay_seconds=10,
            )

        self.assertEqual(response_json, {'choices': []})
        self.assertEqual(attempts, 2)
        sleep_mock.assert_called_once_with(10)

    def test_retries_temporary_server_error_then_returns_response(self) -> None:
        """
        Checks that a temporary server response is retried before returning a successful response.
        """
        url = 'http://127.0.0.1:1234/v1/chat/completions'
        request = httpx.Request('POST', url)
        client = Mock()
        client.post.side_effect = [
            httpx.Response(503, json={'error': 'Model loading'}, request=request),
            httpx.Response(200, json={'choices': []}, request=request),
        ]

        with patch.object(promptfoo_provider.time, 'sleep') as sleep_mock:
            response_json, attempts = promptfoo_provider._post_chat_completion_with_retries(
                client,
                url,
                {},
                {},
                max_attempts=2,
                retry_delay_seconds=10,
            )

        self.assertEqual(response_json, {'choices': []})
        self.assertEqual(attempts, 2)
        sleep_mock.assert_called_once_with(10)

    def test_reports_connection_error_after_final_attempt(self) -> None:
        """
        Checks that repeated connection failures report the total number of attempts.
        """
        url = 'http://127.0.0.1:1234/v1/chat/completions'
        request = httpx.Request('POST', url)
        client = Mock()
        client.post.side_effect = [
            httpx.ConnectError('Connection refused', request=request),
            httpx.ConnectError('Connection refused', request=request),
        ]

        with (
            patch.object(promptfoo_provider.time, 'sleep') as sleep_mock,
            self.assertRaisesRegex(RuntimeError, 'after 2 attempt') as context,
        ):
            promptfoo_provider._post_chat_completion_with_retries(
                client,
                url,
                {},
                {},
                max_attempts=2,
                retry_delay_seconds=10,
            )

        self.assertIn('Connection refused', str(context.exception))
        sleep_mock.assert_called_once_with(10)
