import random
import unittest

from easyqueue.core.objects.base.eqshardedobject_schema import EqShardedObjectSchema


class TestEqShardedObjectSchema(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_validate_ok(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'h3': 'FFFFFFF'
        }
        expected_res = {}

        validator = EqShardedObjectSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_region(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': '',
            'h3': 'FFFFFFF'
        }
        expected_res = {'region': ['Invalid empty field']}

        validator = EqShardedObjectSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_h3(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'h3': ''
        }
        expected_res = {'h3': ['Invalid empty field']}

        validator = EqShardedObjectSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)
