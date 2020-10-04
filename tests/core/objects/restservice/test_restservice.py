import unittest
from datetime import datetime
import random

from easyqueue.core.objects.rest import RestService


class TestRestService(unittest.TestCase):

    def setUp(self):
        random.seed(5432)

    def test_init_ok(self):
        identificator = 'identificator'
        host = 'host'
        port = 15000
        context_path = '/context'
        expected_id = '541028a93b1c3607b67cdf7394af4e67'
        expected_identificator = 'identificator'
        expected_host = 'host'
        expected_port = 15000
        expected_context_path = '/context'
        expected_hostport = 'host:15000'
        expected_uri = 'host:15000/context'

        time_before_creation = datetime.utcnow().timestamp()
        res = RestService(identificator=identificator, host=host, port=port, context_path=context_path)
        time_after_creation = datetime.utcnow().timestamp()

        self.assertEqual(res.identificator, expected_identificator)
        self.assertEqual(res.id, expected_id)
        self.assertTrue(time_before_creation <= res.created_at <= time_after_creation)
        self.assertEqual(res.host, expected_host)
        self.assertEqual(res.port, expected_port)
        self.assertEqual(res.context_path, expected_context_path)
        self.assertEqual(res.hostport, expected_hostport)
        self.assertEqual(res.uri, expected_uri)

    def test_init_ko(self):
        expected_msg = '{\'host\': [\'Invalid empty field\'], \'identificator\': [\'Invalid empty field\']}'

        with self.assertRaises(Exception) as exp:
            RestService(identificator='', host='')
        self.assertEqual(str(exp.exception), expected_msg)

    def test_json_ok(self):
        identificator = 'identificator'
        host = 'host'
        port = 15000
        context_path = '/context'
        expected_res = {
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'id': '541028a93b1c3607b67cdf7394af4e67',
            'host': 'host',
            'port': 15000,
            'context_path': '/context'
        }

        res = RestService(identificator=identificator, host=host, port=port, context_path=context_path).json()

        self.assertAlmostEqual(res['created_at'], expected_res['created_at'])
        self.assertEqual(res['identificator'], expected_res['identificator'])
        self.assertEqual(res['id'], expected_res['id'])
        self.assertEqual(res['host'], expected_res['host'])
        self.assertEqual(res['port'], expected_res['port'])
        self.assertEqual(res['context_path'], expected_res['context_path'])

    def test_from_json_ok(self):
        data = {
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'id': ' 541028a93b1c3607b67cdf7394af4e67',
            'host': 'host',
            'port': 15000,
            'context_path': '/context'
        }

        res = RestService.from_json(obj=data)
        self.assertEqual(res.json(), data)

    def test_from_json_ko(self):
        data = {
            'identificator': 'identificator',
            'created_at': datetime.utcnow().timestamp(),
            'id': '5eff1410425d349daf4a744a881f79fa',
            'host': 'host'
        }
        expected_msg = '{\'context_path\': [\'Missing data for required field.\']}'

        with self.assertRaises(ValueError) as exp:
            RestService.from_json(obj=data)
        self.assertEqual(str(exp.exception), expected_msg)

    def test_validate_ok(self):
        res = RestService(identificator='identificator', host='host')
        self.assertIsNone(res.validate())

    def test_validate_ko(self):
        expected_msg = '{\'id\': [\'Invalid generated id\']}'

        res = RestService(identificator='identificator', host='host')
        res.identificator = 'other'
        with self.assertRaises(ValueError) as exp:
            res.validate()
        self.assertEqual(str(exp.exception), expected_msg)


if __name__ == '__main__':
    unittest.main()
