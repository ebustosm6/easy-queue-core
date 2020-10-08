import random
import unittest

from easyqueue.core.objects.ticket.ticket_schema import TicketSchema


class TestTicketSchema(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_validate_ok(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'h3': 'FFFFFFF',
            'user_id': 'user_id',
            'user_identificator': 'user_identificator',
            'queue_id': 'queue_id',
            'queue_identificator': 'queue_identificator',
            'is_active': True,
        }
        expected_res = {}

        validator = TicketSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_user_id(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'h3': 'FFFFFFF',
            'user_id': '',
            'user_identificator': 'user_identificator',
            'queue_id': 'queue_id',
            'queue_identificator': 'queue_identificator',
            'is_active': True,
        }
        expected_res = {'user_id': ['Invalid empty field']}

        validator = TicketSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_user_identificator(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'h3': 'FFFFFFF',
            'user_id': 'user_id',
            'user_identificator': '',
            'queue_id': 'queue_id',
            'queue_identificator': 'queue_identificator',
            'is_active': True,
        }
        expected_res = {'user_identificator': ['Invalid empty field']}

        validator = TicketSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_queue_id(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'h3': 'FFFFFFF',
            'user_id': 'user_id',
            'user_identificator': 'user_identificator',
            'queue_id': '',
            'queue_identificator': 'queue_identificator',
            'is_active': True,
        }
        expected_res = {'queue_id': ['Invalid empty field']}

        validator = TicketSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)

    def test_validate_ko_invalid_queue_identificator(self):
        data = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            'identificator': 'identificator',
            'created_at': 1590000000.000000,
            'region': 'region',
            'h3': 'FFFFFFF',
            'user_id': 'user_id',
            'user_identificator': 'user_identificator',
            'queue_id': 'queue_id',
            'queue_identificator': '',
            'is_active': True,
        }
        expected_res = {'queue_identificator': ['Invalid empty field']}

        validator = TicketSchema()
        res = validator.validate(data=data)
        self.assertEqual(res, expected_res)
