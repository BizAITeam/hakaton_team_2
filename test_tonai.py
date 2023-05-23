import unittest
from unittest.mock import patch

import requests
from requests.exceptions import RequestException

from tonai import TonAI, check_url_exists

class TonAITest(unittest.TestCase):

    def test_init_valid(self):
        tonai = TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=0.6, service_name='chat')
        self.assertEqual(tonai.tonai_api_key, 'api_key')
        self.assertEqual(tonai.endpoint_url, 'https://example.com')
        self.assertEqual(tonai.temperature, 0.6)
        self.assertEqual(tonai.service_name, 'chat')

    def test_init_invalid_service_name(self):
        with self.assertRaises(ValueError):
            TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=0.6, service_name='invalid')

    def test_init_invalid_tonai_api_key(self):
        with self.assertRaises(ValueError):
            TonAI(tonai_api_key=123, endpoint_url='https://example.com', temperature=0.6, service_name='chat')

    def test_init_empty_tonai_api_key(self):
        with self.assertRaises(ValueError):
            TonAI(tonai_api_key='', endpoint_url='https://example.com', temperature=0.6, service_name='chat')

    def test_init_invalid_endpoint_url(self):
        with self.assertRaises(ValueError):
            TonAI(tonai_api_key='api_key', endpoint_url='invalid_url', temperature=0.6, service_name='chat')

    def test_init_invalid_temperature(self):
        with self.assertRaises(ValueError):
            TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=-0.6, service_name='chat')

    def test_init_invalid_url_not_accessible(self):
        with patch('requests.get', side_effect=requests.exceptions.RequestException):
            with self.assertRaises(ValueError):
                TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=0.6, service_name='chat')

    def test_check_url_exists(self):
        self.assertTrue(check_url_exists('https://example.com'))
        self.assertFalse(check_url_exists('https://nonexistent.com'))

    @patch('requests.post')
    def test_call(self, mock_post):
        mock_post.return_value.text = '{"messages": [{"text": "response_text"}]}'

        tonai = TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=0.6, service_name='chat')
        message = "input_message"
        response = tonai._call(message)

        self.assertEqual(response, 'response_text')

    def test_call_empty_endpoint_url(self):
        tonai = TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=0.6, service_name='chat')
        tonai.endpoint_url = ''
        with self.assertRaises(ValueError):
            tonai._call('input_message')

    def test_call_invalid_endpoint_url(self):
        tonai = TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=0.6, service_name='chat')
        tonai.endpoint_url = 'invalid_url'
        with self.assertRaises(ValueError):
            tonai._call('input_message')

    @patch('requests.post', side_effect=RequestException('Error'))
    def test_call_request_exception(self, mock_post):
        tonai = TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=0.6, service_name='chat')
        with self.assertRaises(ValueError):
            tonai._call('input_message')

    @patch('requests.post')
    def test_call_error_in_response(self, mock_post):
        mock_post.return_value.text = '{"error": "response_error"}'

        tonai = TonAI(tonai_api_key='api_key', endpoint_url='https://example.com', temperature=0.6, service_name='chat')
        with self.assertRaises(ValueError):
            tonai._call('input_message')

if __name__ == '__main__':
    unittest.main()
