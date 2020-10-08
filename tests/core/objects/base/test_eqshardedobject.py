import unittest
from datetime import datetime
import random

from easyqueue.core.objects.base.eqshardedobject import EqShardedObject

from easyqueue.core.objects.queue.queue import Queue


class TestEqShardedObject(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_init_ok(self):
        identificator = 'identificator'
        region = 'region'
        h3 = 'FFFFFFF'
        expected_id = '84c5bdb20a4c364e8a9bb75f789c75fa'
        expected_identificator = 'identificator'
        expected_region = 'region'
        expected_h3 = 'FFFFFFF'

        time_before_creation = datetime.utcnow().timestamp()
        res = EqShardedObject(identificator=identificator, h3=h3, region=region)
        time_after_creation = datetime.utcnow().timestamp()

        self.assertEqual(res.identificator, expected_identificator)
        self.assertEqual(res._id, expected_id)
        self.assertTrue(time_before_creation <= res.created_at <= time_after_creation)
        self.assertEqual(res.region, expected_region)
        self.assertEqual(res.h3, expected_h3)

    def test_init_ko(self):
        expected_msg = {
            'h3': ['Invalid empty field'],
            'identificator': ['Invalid empty field'],
            'region': ['Invalid empty field']
        }

        with self.assertRaises(Exception) as exp:
            EqShardedObject(identificator='', region='', h3='')
        self.assertDictEqual(exp.exception.args[0], expected_msg)

    def test_json_ok(self):
        identificator = 'identificator'
        region = 'region'
        h3 = 'FFFFFFF'
        expected_res = {
            '_id': '84c5bdb20a4c364e8a9bb75f789c75fa',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'region': 'region',
            'h3': 'FFFFFFF'
        }

        res = EqShardedObject(identificator=identificator, region=region, h3=h3).json()

        self.assertAlmostEqual(res['created_at'], expected_res['created_at'])
        self.assertEqual(res['identificator'], expected_res['identificator'])
        self.assertEqual(res['_id'], expected_res['_id'])
        self.assertEqual(res['region'], expected_res['region'])
        self.assertEqual(res['h3'], expected_res['h3'])

    def test_from_json_ok(self):
        data = {
            '_id': '94a290623fe33e36adc13a0aac7f2974',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'region': 'region',
            'h3': 'FFFFFFF'
        }

        res = EqShardedObject.from_json(obj=data)
        self.assertEqual(res.json(), data)

    def test_from_json_ko(self):
        data = {
            '_id': '94a290623fe33e36adc13a0aac7f2974',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'h3': 'FFFFFFF'
        }
        expected_msg = {
            'region': ['Missing data for required field.']
        }

        with self.assertRaises(ValueError) as exp:
            EqShardedObject.from_json(obj=data)
        self.assertEqual(exp.exception.args[0], expected_msg)

    def test_validate_ok(self):
        res = EqShardedObject(identificator='identificator', region='region', h3='FFFFFFF')
        self.assertIsNone(res.validate())

    def test_validate_ko(self):
        expected_msg = {
            '_id': ['Invalid generated id']
        }

        res = EqShardedObject(identificator='identificator', region='region', h3='FFFFFFF')
        res.identificator = 'other'
        with self.assertRaises(ValueError) as exp:
            res.validate()
        self.assertEqual(exp.exception.args[0], expected_msg)


if __name__ == '__main__':
    unittest.main()
