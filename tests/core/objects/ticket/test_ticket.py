import unittest
from datetime import datetime
import random

from easyqueue.core.objects.ticket.ticket import Ticket


class TestTicket(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_init_ok(self):
        user_id = 'user_id'
        user_identificator = 'user_identificator'
        region = 'region'
        queue_id = 'queue_id'
        queue_identificator = 'queue_identificator'
        is_active = True
        expected_id = '891e731c0a733f9fb10ec8c575c4f199'
        expected_identificator = 'ticket_region_user_identificator_queue_identificator'
        expected_user_id = 'user_id'
        expected_user_identificator = 'user_identificator'
        expected_region = 'region'
        expected_queue_id = 'queue_id'
        expected_queue_identificator = 'queue_identificator'
        expected_is_active = True

        time_before_creation = datetime.utcnow().timestamp()
        res = Ticket(
            user_id=user_id, user_identificator=user_identificator, region=region,
            queue_id=queue_id, queue_identificator=queue_identificator, is_active=is_active)
        time_after_creation = datetime.utcnow().timestamp()

        self.assertEqual(res.identificator, expected_identificator)
        self.assertEqual(res._id, expected_id)
        self.assertTrue(time_before_creation <= res.created_at <= time_after_creation)
        self.assertEqual(res.user_id, expected_user_id)
        self.assertEqual(res.user_identificator, expected_user_identificator)
        self.assertEqual(res.region, expected_region)
        self.assertEqual(res.queue_id, expected_queue_id)
        self.assertEqual(res.queue_identificator, expected_queue_identificator)
        self.assertEqual(res.is_active, expected_is_active)

    def test_init_ko(self):
        expected_msg = '{\'identificator\': [\'Invalid double punctuation character "_"\'], ' \
                        '\'queue_id\': [\'Invalid empty field\'], ' \
                        '\'queue_identificator\': [\'Invalid empty field\'], ' \
                        '\'region\': [\'Invalid empty field\'], ' \
                        '\'user_id\': [\'Invalid empty field\'], ' \
                        '\'user_identificator\': [\'Invalid empty field\']}'

        with self.assertRaises(Exception) as exp:
            Ticket(user_id='', user_identificator='', region='', queue_id='', queue_identificator='')
        self.assertEqual(str(exp.exception), expected_msg)

    def test_json_ok(self):
        user_id = 'user_id'
        user_identificator = 'user_identificator'
        region = 'region'
        queue_id = 'queue_id'
        queue_identificator = 'queue_identificator'
        is_active = True
        expected_res = {
            '_id': '891e731c0a733f9fb10ec8c575c4f199',
            'identificator': 'ticket_region_user_identificator_queue_identificator',
            'created_at': datetime.utcnow().timestamp(),
            'region': 'region',
            'user_id': 'user_id',
            'user_identificator': 'user_identificator',
            'queue_id': 'queue_id',
            'queue_identificator': 'queue_identificator',
            'is_active': True,
        }

        res = Ticket(
            user_id=user_id, user_identificator=user_identificator, region=region,
            queue_id=queue_id, queue_identificator=queue_identificator, is_active=is_active).json()

        self.assertAlmostEqual(res['created_at'], expected_res['created_at'])
        self.assertEqual(res['identificator'], expected_res['identificator'])
        self.assertEqual(res['_id'], expected_res['_id'])
        self.assertEqual(res['user_id'], expected_res['user_id'])
        self.assertEqual(res['user_identificator'], expected_res['user_identificator'])
        self.assertEqual(res['region'], expected_res['region'])
        self.assertEqual(res['queue_id'], expected_res['queue_id'])
        self.assertEqual(res['queue_identificator'], expected_res['queue_identificator'])

    def test_from_json_ok(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'user_id': 'user_id',
            'user_identificator': 'user_identificator',
            'queue_id': 'queue_id',
            'queue_identificator': 'queue_identificator',
            'is_active': True,
        }

        res = Ticket.from_json(obj=data)
        self.assertEqual(res.json(), data)

    def test_from_json_ko(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'user_id': 'user_id',
            'user_identificator': 'user_identificator',
            'queue_id': 'queue_id',
            'queue_identificator': 'queue_identificator',
            'is_active': True,
        }
        expected_msg = '{\'region\': [\'Missing data for required field.\']}'

        with self.assertRaises(ValueError) as exp:
            Ticket.from_json(obj=data)
        self.assertEqual(str(exp.exception), expected_msg)

    def test_validate_ok(self):
        res = Ticket(
            user_id='user_id', user_identificator='user_identificator',
            region='region', queue_id='queue_id', queue_identificator='queue_identificator'
        )
        self.assertIsNone(res.validate())

    def test_validate_ko(self):
        expected_msg = '{\'_id\': [\'Invalid generated id\']}'

        res = Ticket(
            user_id='user_id', user_identificator='user_identificator',
            region='region', queue_id='queue_id', queue_identificator='queue_identificator'
        )
        res.user_id = 'other'
        with self.assertRaises(ValueError) as exp:
            res.validate()
        self.assertEqual(str(exp.exception), expected_msg)


if __name__ == '__main__':
    unittest.main()
