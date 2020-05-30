import random
import unittest

from easyqueue.core.objects.base.schema import EQObjectSchema


class TestEQObjectSchema(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_validate_ok(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000
        }
        expected_res = {}

        validator = EQObjectSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_id(self):
        data = {
            'id': '',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
        }
        expected_res = {'id': ['Invalid empty field']}

        validator = EQObjectSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_identificator(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': '',
            'created_at': 1590000000.000000,
        }
        expected_res = {'identificator': ['Invalid empty field']}

        validator = EQObjectSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_created_at(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 150000.000000,
        }
        expected_res = {'created_at': ['Invalid value field']}

        validator = EQObjectSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)
