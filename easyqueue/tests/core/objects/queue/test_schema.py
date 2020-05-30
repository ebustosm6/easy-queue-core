import random
import unittest

from easyqueue.core.objects.queue.schema import QueueSchema


class TestQueueSchema(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_validate_ok(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'user_id': 'user_id',
            'group': 'group',
            'info': '',
            'tags': set(),
            'limit': 0,
            'is_active': True,
            'image': 'image'
        }
        expected_res = {}

        validator = QueueSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_region(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': '',
            'user_id': 'user_id',
            'group': 'group',
            'info': 'info',
            'tags': set(),
            'limit': 0,
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'region': ['Invalid empty field']}

        validator = QueueSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_user_id(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'user_id': '',
            'group': 'group',
            'info': 'info',
            'tags': set(),
            'limit': 0,
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'user_id': ['Invalid empty field']}

        validator = QueueSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_group(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'user_id': 'user_id',
            'group': '',
            'info': 'info',
            'tags': set(),
            'limit': 0,
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'group': ['Invalid empty field']}

        validator = QueueSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_tags(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'user_id': 'user_id',
            'group': 'group',
            'info': 'info',
            'tags': 3,
            'limit': 0,
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'tags': ['Not a valid list.']}

        validator = QueueSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_limit(self):
        data = {
            'id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'user_id': 'user_id',
            'group': 'group',
            'info': 'info',
            'tags': set(),
            'limit': -1,
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'limit': ['Limit must be greater than 0 (0 no limit)']}

        validator = QueueSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)
