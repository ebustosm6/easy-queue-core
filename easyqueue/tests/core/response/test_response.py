import unittest

from easyqueue.core.response import ResponseDTO
from easyqueue.core.response import ResponseCode


class TestRepositoryResponse(unittest.TestCase):

    def test_init(self):
        response = ResponseDTO(code=ResponseCode.OK, msg='success', data=6)
        self.assertEqual(ResponseCode.OK, response.code)
        self.assertEqual('success', response.msg)
        self.assertEqual(6, response.data)

    def test_str(self):
        response_str = str(ResponseDTO(code=ResponseCode.OK, msg='success', data=6))
        expected_str = 'RepositoryResponse(code=ResponseCode.OK[1], msg="success", data_type="int")'
        self.assertEqual(expected_str, response_str)

    def test_eq(self):
        response1 = ResponseDTO(code=ResponseCode.OK, msg='success', data=6)
        response2 = ResponseDTO(code=ResponseCode.OK, msg='success', data=6)
        self.assertTrue(response1 == response2)
