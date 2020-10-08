import unittest
from datetime import datetime
import random

from easyqueue.core.objects.queue.queue import Queue


class TestQueue(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_init_ok(self):
        identificator = 'identificator'
        user_id = 'user_id'
        region = 'region'
        h3 = 'FFFFFFF'
        group = 'group'
        info = 'info'
        tags = ['tag1']
        limit = 0
        is_active = True
        image = 'image'
        expected_id = '5dd10a7b7455321c9ff97c50e45a9b4a'
        expected_identificator = 'identificator'
        expected_user_id = 'user_id'
        expected_region = 'region'
        expected_h3 = 'FFFFFFF'
        expected_group = 'group'
        expected_info = 'info'
        expected_tags = ['tag1']
        expected_limit = 0
        expected_is_active = True
        expected_image = 'image'

        time_before_creation = datetime.utcnow().timestamp()
        res = Queue(
            identificator=identificator, h3=h3, user_id=user_id, region=region, group=group, info=info, tags=tags, limit=limit,
            is_active=is_active, image=image
        )
        time_after_creation = datetime.utcnow().timestamp()

        self.assertEqual(res.identificator, expected_identificator)
        self.assertEqual(res._id, expected_id)
        self.assertTrue(time_before_creation <= res.created_at <= time_after_creation)
        self.assertEqual(res.user_id, expected_user_id)
        self.assertEqual(res.region, expected_region)
        self.assertEqual(res.h3, expected_h3)
        self.assertEqual(res.group, expected_group)
        self.assertEqual(res.info, expected_info)
        self.assertEqual(res.tags, expected_tags)
        self.assertEqual(res.limit, expected_limit)
        self.assertEqual(res.is_active, expected_is_active)
        self.assertEqual(res.image, expected_image)

    def test_init_ko(self):
        expected_msg = {
            'h3': ['Invalid empty field'],
            'identificator': ['Invalid empty field'],
            'region': ['Invalid empty field'], 'user_id': ['Invalid empty field']
        }

        with self.assertRaises(Exception) as exp:
            Queue(identificator='', region='', h3='', user_id='')
        self.assertEqual(exp.exception.args[0], expected_msg)

    def test_json_ok(self):
        identificator = 'identificator'
        region = 'region'
        h3 = 'FFFFFFF'
        user_id = 'user_id'
        group = 'group'
        info = ''
        tags = set()
        limit = 0
        is_active = True
        image = 'image'
        expected_res = {
            '_id': '5dd10a7b7455321c9ff97c50e45a9b4a',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'region': 'region',
            'h3': 'FFFFFFF',
            'user_id': 'user_id',
            'group': 'group',
            'info': '',
            'tags': set(),
            'limit': 0,
            'is_active': True,
            'image': 'image'
        }

        res = Queue(identificator=identificator, region=region, h3=h3, user_id=user_id, group=group, info=info,
                    tags=tags, limit=limit, is_active=is_active, image=image).json()

        self.assertAlmostEqual(res['created_at'], expected_res['created_at'])
        self.assertEqual(res['identificator'], expected_res['identificator'])
        self.assertEqual(res['_id'], expected_res['_id'])
        self.assertEqual(res['region'], expected_res['region'])
        self.assertEqual(res['h3'], expected_res['h3'])
        self.assertEqual(res['user_id'], expected_res['user_id'])
        self.assertEqual(res['group'], expected_res['group'])
        self.assertEqual(res['info'], expected_res['info'])
        self.assertEqual(res['tags'], expected_res['tags'])
        self.assertEqual(res['limit'], expected_res['limit'])
        self.assertEqual(res['is_active'], expected_res['is_active'])
        self.assertEqual(res['image'], expected_res['image'])

    def test_from_json_ok(self):
        data = {
            '_id': '94a290623fe33e36adc13a0aac7f2974',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'region': 'region',
            'h3': 'FFFFFFF',
            'user_id': 'user_id',
            'group': 'group',
            'info': '',
            'tags': set(),
            'limit': 0,
            'is_active': True,
            'image': 'image'
        }

        res = Queue.from_json(obj=data)
        self.assertEqual(res.json(), data)

    def test_from_json_ko(self):
        data = {
            '_id': '94a290623fe33e36adc13a0aac7f2974',
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'user_id': 'user_id',
            'group': 'group',
            'info': '',
            'tags': set(),
            'limit': 0,
            'is_active': True,
            'image': 'image'
        }
        expected_msg = {
            'h3': ['Missing data for required field.'],
            'region': ['Missing data for required field.']
        }

        with self.assertRaises(ValueError) as exp:
            Queue.from_json(obj=data)
        self.assertDictEqual(exp.exception.args[0], expected_msg)

    def test_validate_ok(self):
        res = Queue(identificator='identificator', region='region', h3='FFFFFFF', user_id='user_id')
        self.assertIsNone(res.validate())

    def test_validate_ko(self):
        expected_msg = {
            '_id': ['Invalid generated id']
        }

        res = Queue(identificator='identificator', region='region', h3='FFFFFFF', user_id='user_id')
        res.identificator = 'other'
        with self.assertRaises(ValueError) as exp:
            res.validate()
        self.assertEqual(exp.exception.args[0], expected_msg)


if __name__ == '__main__':
    unittest.main()
