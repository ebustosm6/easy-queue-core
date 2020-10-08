import unittest
from datetime import datetime
import random

from easyqueue.core.objects.user.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_init_ok(self):
        identificator = 'identificator'
        email = 'email@server.dom'
        region = 'region'
        h3 = 'FFFFFFF'
        password = 'password'
        is_active = True
        image = 'image'
        expected_id = '080148b36ee238bab9e84bde3ea94f11'
        expected_identificator = 'identificator'
        expected_email = 'email@server.dom'
        expected_region = 'region'
        expected_password = 'password'
        expected_is_active = True
        expected_image = 'image'

        time_before_creation = datetime.utcnow().timestamp()
        res = User(identificator=identificator, email=email, region=region, h3=h3,
                   password=password, is_active=is_active, image=image)
        time_after_creation = datetime.utcnow().timestamp()

        self.assertEqual(res.identificator, expected_identificator)
        self.assertEqual(res._id, expected_id)
        self.assertTrue(time_before_creation <= res.created_at <= time_after_creation)
        self.assertEqual(res.email, expected_email)
        self.assertEqual(res.region, expected_region)
        self.assertEqual(res.password, expected_password)
        self.assertEqual(res.is_active, expected_is_active)
        self.assertEqual(res.image, expected_image)

    def test_init_ko(self):
        expected_msg = {
            'email': ['Invalid empty field'],
            'identificator': ['Invalid empty field'],
            'password': ['Invalid empty field'],
            'region': ['Invalid empty field'],
            'h3': ['Invalid empty field']
        }

        with self.assertRaises(Exception) as exp:
            User(identificator='', email='', region='', password='', h3='')
        self.assertEqual(exp.exception.args[0], expected_msg)

    def test_json_ok(self):
        identificator = 'identificator'
        email = 'email@server.dom'
        region = 'region'
        h3 = 'FFFFFFF'
        password = 'password'
        is_active = True
        image = 'image'
        expected_res = {
            '_id': '080148b36ee238bab9e84bde3ea94f11',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'email': 'email@server.dom',
            'password': 'password',
            'region': 'region',
            'h3': 'FFFFFFF',
            'is_active': True,
            'image': 'image'
        }

        res = User(identificator=identificator, email=email, region=region, h3=h3,
                   password=password, is_active=is_active, image=image).json()

        self.assertAlmostEqual(res['created_at'], expected_res['created_at'])
        self.assertEqual(res['identificator'], expected_res['identificator'])
        self.assertEqual(res['_id'], expected_res['_id'])
        self.assertEqual(res['email'], expected_res['email'])
        self.assertEqual(res['password'], expected_res['password'])
        self.assertEqual(res['region'], expected_res['region'])
        self.assertEqual(res['h3'], expected_res['h3'])

    def test_from_json_ok(self):
        data = {
            '_id': '080148b36ee238bab9e84bde3ea94f11',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'email': 'email@server.dom',
            'password': 'password',
            'region': 'region',
            'h3': 'FFFFFFF',
            'is_active': True,
            'image': 'image'
        }

        res = User.from_json(obj=data)
        self.assertEqual(res.json(), data)

    def test_from_json_ko(self):
        data = {
            '_id': '080148b36ee238bab9e84bde3ea94f11',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'email': 'email@server.dom',
            'region': 'region',
            'h3': 'FFFFFFF',
            'is_active': True,
            'image': 'image'
        }
        expected_msg = {
            'password': ['Missing data for required field.']
        }

        with self.assertRaises(ValueError) as exp:
            User.from_json(obj=data)
        self.assertDictEqual(exp.exception.args[0], expected_msg)

    def test_validate_ok(self):
        res = User(identificator='identificator', email='email@server.dom', region='region', h3='FFFFFFF',
                   password='password', is_active=True, image='image')
        self.assertIsNone(res.validate())

    def test_validate_ko(self):
        expected_msg = {
            '_id': ['Invalid generated id']
        }

        res = User(identificator='identificator', email='email@server.dom', region='region', h3='FFFFFFF',
                   password='password', is_active=True, image='image')
        res.identificator = 'other'
        with self.assertRaises(ValueError) as exp:
            res.validate()
        self.assertEqual(exp.exception.args[0], expected_msg)


if __name__ == '__main__':
    unittest.main()
