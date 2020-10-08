import random
import unittest

from easyqueue.core.objects.user.user_schema import UserSchema


class TestUserSchema(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_validate_ok(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'email': 'email@server.dom',
            'password': 'password',
            'region': 'region',
            'h3': 'FFFFFFF',
            'is_active': True,
            'image': 'image'
        }
        expected_res = {}

        validator = UserSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_region(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'email': 'email@server.dom',
            'password': 'password',
            'region': '',
            'h3': 'FFFFFFF',
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'region': ['Invalid empty field']}

        validator = UserSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_h3(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'email': 'email@server.dom',
            'password': 'password',
            'region': 'region',
            'h3': '',
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'h3': ['Invalid empty field']}

        validator = UserSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_email(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'email': 'invalid_email',
            'password': 'password',
            'region': 'region',
            'h3': 'FFFFFFF',
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'email': ['Invalid email pattern, must math <name>@<server>.<domain>']}

        validator = UserSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_password(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'email': 'email@server.dom',
            'password': '',
            'region': 'region',
            'h3': 'FFFFFFF',
            'is_active': True,
            'image': 'image'
        }
        expected_res = {'password': ['Invalid empty field']}

        validator = UserSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)
