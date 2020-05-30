import unittest
from datetime import datetime
import random

from easyqueue.core.objects.base.eqobject import EQObject


class TestEQObject(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_init_ok(self):
        identificator = 'identificator'
        expected_id = 'a9a6452334e33ced8e5edb70a01a773e'
        expected_identificator = 'identificator'

        time_before_creation = datetime.utcnow().timestamp()
        res = EQObject(identificator=identificator)
        time_after_creation = datetime.utcnow().timestamp()

        self.assertEqual(res.identificator, expected_identificator)
        self.assertEqual(res.id, expected_id)
        self.assertTrue(time_before_creation <= res.created_at <= time_after_creation)

    def test_init_ko(self):
        expected_msg = '{\'identificator\': [\'Invalid empty field\']}'

        with self.assertRaises(Exception) as exp:
            EQObject(identificator='')
        self.assertEqual(str(exp.exception), expected_msg)

    def test_json_ok(self):
        identificator = 'identificator'
        expected_res = {
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'id': 'a9a6452334e33ced8e5edb70a01a773e',
        }

        res = EQObject(identificator=identificator).json()

        self.assertAlmostEqual(res['created_at'], expected_res['created_at'])
        self.assertEqual(res['identificator'], expected_res['identificator'])
        self.assertEqual(res['id'], expected_res['id'])

    def test_from_json_ok(self):
        data = {
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'id': '5eff1410425d349daf4a744a881f79fa',
        }

        res = EQObject.from_json(obj=data)
        self.assertEqual(res.json(), data)

    def test_from_json_ko(self):
        data = {
            'created_at': datetime.utcnow().timestamp(),
            'id': '5eff1410425d349daf4a744a881f79fa',
        }
        expected_msg = '{\'identificator\': [\'Missing data for required field.\']}'

        with self.assertRaises(ValueError) as exp:
            EQObject.from_json(obj=data)
        self.assertEqual(str(exp.exception), expected_msg)

    def test_validate_ok(self):
        res = EQObject(identificator='identificator')
        self.assertIsNone(res.validate())

    def test_validate_ko(self):
        expected_msg = '{\'id\': [\'Invalid generated id\']}'

        res = EQObject(identificator='identificator')
        res.identificator = 'other'
        with self.assertRaises(ValueError) as exp:
            res.validate()
        self.assertEqual(str(exp.exception), expected_msg)


if __name__ == '__main__':
    unittest.main()
