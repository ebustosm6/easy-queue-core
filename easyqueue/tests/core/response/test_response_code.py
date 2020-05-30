import unittest

from easyqueue.core.response import ResponseCode


class TestResponseCode(unittest.TestCase):

    def test_codes(self):
        self.assertEqual(0, ResponseCode.UNEXPECTED_ERROR.value)
        self.assertEqual('UNEXPECTED_ERROR', ResponseCode.UNEXPECTED_ERROR.name)

        self.assertEqual(1, ResponseCode.OK.value)
        self.assertEqual('OK', ResponseCode.OK.name)

        self.assertEqual(2, ResponseCode.PARTIAL_RESPONSE.value)
        self.assertEqual('PARTIAL_RESPONSE', ResponseCode.PARTIAL_RESPONSE.name)

        self.assertEqual(3, ResponseCode.CONNECTION_ERROR.value)
        self.assertEqual('CONNECTION_ERROR', ResponseCode.CONNECTION_ERROR.name)

        self.assertEqual(4, ResponseCode.INVALID_REQUEST.value)
        self.assertEqual('INVALID_REQUEST', ResponseCode.INVALID_REQUEST.name)

        self.assertEqual(5, ResponseCode.OPERATION_ERROR.value)
        self.assertEqual('OPERATION_ERROR', ResponseCode.OPERATION_ERROR.name)

        self.assertEqual(6, ResponseCode.AUTHENTICATION_ERROR.value)
        self.assertEqual('AUTHENTICATION_ERROR', ResponseCode.AUTHENTICATION_ERROR.name)

        self.assertEqual(7, ResponseCode.NO_CONTENT.value)
        self.assertEqual('NO_CONTENT', ResponseCode.NO_CONTENT.name)
