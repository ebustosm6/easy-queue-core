import unittest

from pymongo.errors import ConnectionFailure, WriteError

from easyqueue.core.response import ResponseCode, ResponseDTO
from easyqueue.database.mongo.exception_mapper import MongoExceptionMapper


class TestMongoExceptionMapper(unittest.TestCase):

    def test_database_response_code(self):
        exception = ConnectionFailure(message='Not possible to connect with db')
        expected_result_code = ResponseCode.CONNECTION_ERROR
        result_code = MongoExceptionMapper.response_code(exception)
        self.assertEqual(expected_result_code, result_code)

    def test_database_response_code_parent(self):
        exception = WriteError(error='Not possible to write in db')
        expected_result_code = ResponseCode.OPERATION_ERROR
        result_code = MongoExceptionMapper.response_code(exception)
        self.assertEqual(expected_result_code, result_code)

    def test_generate_error_response(self):
        exception = ConnectionFailure(message='Not possible to connect with db')
        expected_result_response = ResponseDTO(code=ResponseCode.CONNECTION_ERROR,
                                               msg='Not possible to connect with db')
        result_response = MongoExceptionMapper.generate_error_response(exception)
        self.assertEqual(expected_result_response, result_response)
