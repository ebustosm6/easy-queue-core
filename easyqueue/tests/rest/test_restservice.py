import unittest
import copy

from easyqueue.rest import RestService


class TestEQObject(unittest.TestCase):

    def setUp(self):
        self.example_restservice_json = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ed',
            '__type__': 'RestService',
            '_created_at': '2020-02-03T16:57:53.501633',
            '_host': 'exampleservice',
            '_port': 12345,
            '_context_path': '/'
        }

        self.example_restservice = RestService(host='exampleservice')
        self.example_restservice.__dict__ = copy.deepcopy(self.example_restservice_json)

    def test_init(self):
        self.assertEqual(self.example_restservice.id, self.example_restservice_json['_id'])
        self.assertEqual(type(self.example_restservice), RestService)
        self.assertEqual(self.example_restservice.created_at, self.example_restservice_json['_created_at'])

    def test_host(self):
        self.assertEqual(self.example_restservice_json['_host'], self.example_restservice.host)

    def test_port(self):
        self.assertEqual(self.example_restservice_json['_port'], self.example_restservice.port)

    def test_context_path(self):
        self.assertEqual(self.example_restservice_json['_context_path'], self.example_restservice.context_path)

    def test_hostport(self):
        self.assertEqual('exampleservice:12345', self.example_restservice.hostport)

    def test_uri(self):
        self.assertEqual('exampleservice:12345/', self.example_restservice.uri)

    def test_json(self):
        self.assertEqual(self.example_restservice_json, self.example_restservice.json())

    def test_from_json(self):
        rests_service = RestService.from_json(self.example_restservice_json)
        self.assertEqual(rests_service.id, self.example_restservice.id)
        self.assertEqual(type(rests_service), type(self.example_restservice))
        self.assertEqual(rests_service.__type__, self.example_restservice.__type__)
        self.assertEqual(rests_service.created_at, self.example_restservice.created_at)
        self.assertEqual(rests_service.host, self.example_restservice.host)
        self.assertEqual(rests_service.port, self.example_restservice.port)
        self.assertEqual(rests_service.context_path, self.example_restservice.context_path)
        self.assertEqual(rests_service.hostport, self.example_restservice.hostport)
        self.assertEqual(rests_service.uri, self.example_restservice.uri)
        self.assertEqual(rests_service.json(), self.example_restservice.json())


if __name__ == '__main__':
    unittest.main()
