import unittest
import requests
from unittest import mock

from easyqueue.client.base_client import BaseClient


class RequestMock(mock.Mock):

    @staticmethod
    def request_200(*args, **kwargs):
        response =  requests.Response()
        response.status_code = 200
        return response


class TestBaseClient(unittest.TestCase):

    def test_init(self):
        host = 'host'
        port = 10_000
        protocol = 'http'
        verify = False
        timeout = 10
        proxies = None
        expected_host = 'host'
        expected_port = 10_000
        expected_protocol = 'http'
        expected_verify = False
        expected_timeout = 10
        expected_proxies = None
        expected_debug_trace = []

        client = BaseClient(host=host, port=port, protocol=protocol, verify=verify, timeout=timeout, proxies=proxies)

        self.assertEqual(client.host, expected_host)
        self.assertEqual(client.port, expected_port)
        self.assertEqual(client.protocol, expected_protocol)
        self.assertEqual(client.verify, expected_verify)
        self.assertEqual(client.timeout, expected_timeout)
        self.assertEqual(client.proxies, expected_proxies)
        self.assertEqual(client.debug_trace, expected_debug_trace)

    def test_is_correct_status_code_ok_200(self):
        status_code = 200
        expected_result = True

        client = BaseClient(host='host')
        result = client.is_correct_status_code(status_code)

        self.assertEqual(result, expected_result)

    def test_is_correct_status_code_ok_204(self):
        status_code = 204
        expected_result = True

        client = BaseClient(host='host')
        result = client.is_correct_status_code(status_code)

        self.assertEqual(result, expected_result)

    def test_is_correct_status_code_ok_300(self):
        status_code = 300
        expected_result = False

        client = BaseClient(host='host')
        result = client.is_correct_status_code(status_code)

        self.assertEqual(result, expected_result)

    def test_is_correct_status_code_ko(self):
        status_code = 'invalid'
        expected_error = 'Invalid type for status_code with value invalid, expected int, found str'

        client = BaseClient(host='host')

        with self.assertRaises(TypeError) as exp:
            client.is_correct_status_code(status_code)
            self.assertEqual(str(exp), expected_error)

    @mock.patch('requests.request')
    def test_call(self, mock_requests):
        mock_requests.side_effect = RequestMock.request_200
        expected_status_code = 200

        client = BaseClient(host='host')
        result = client.call(method='GET', url='url')

        self.assertEqual(result.status_code, expected_status_code)

