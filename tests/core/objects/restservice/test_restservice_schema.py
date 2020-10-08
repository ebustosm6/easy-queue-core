import random
import unittest

from easyqueue.core.objects.rest.restservice_schema import RestServiceSchema


class TestRestServiceSchema(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_validate_ok(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'host': 'host',
            'context_path': '/context_path'
        }
        expected_res = {}

        validator = RestServiceSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_host(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'host': '',
            'context_path': '/context_path'
        }
        expected_res = {'host': ['Invalid empty field']}

        validator = RestServiceSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_port(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'host': 'host',
            'port': 1,
            'context_path': '/context_path'
        }
        expected_res = {'port': ['Port must be between 1024 and 49151']}

        validator = RestServiceSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_context_path(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'host': 'host',
            'context_path': 'context_path'
        }
        expected_res = {'context_path': ['Must start with "/"']}

        validator = RestServiceSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)
