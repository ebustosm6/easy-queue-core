import unittest
import asyncio

from schema import SchemaMissingKeyError, Schema, And
from easyqueue.database.mongo import MongoRepository


class TestMongoRepository(unittest.TestCase):

    def setUp(self):
        schema = Schema(
            {
                '_id': And(str, len),
                '_value': And(str, len)
            },
            ignore_extra_keys=False)

        self.repository = MongoRepository(
            uri='mongodb://localhost:27017/', database='test', collection='test', validation_schema=schema)

    @unittest.skip('Development test')
    def test_create_one(self):
        example_element_json = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ew',
            '_value': 'EQObject'
        }

        expected_result = {'acknowledged': True, 'inserted_id': '9c482525eaa14c3d808de7d1d1a483ew'}

        loop = asyncio.get_event_loop()
        result_create = loop.run_until_complete(self.repository.create_one(element=example_element_json))
        self.assertIsInstance(result_create, dict)
        self.assertEqual(expected_result, result_create)

    def test_create_one_invalid_element_type(self):
        example_element_json = {
            '_id': '9c482525eaa14c3d808de7d1d1a483ew',
            '_value': 'EQObject'
        }

        expected_error_msg = 'element not valid: must be dict'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.create_one(element=str(example_element_json)))

        self.assertEqual(expected_error_msg, str(exc.exception))

    def test_create_one_invalid_element_value(self):
        example_element_json = {
            '_value': 'EQObject'
        }

        expected_error_msg = 'Missing key: \'_id\''

        with self.assertRaises(SchemaMissingKeyError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.create_one(element=example_element_json, validate=True))

        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_create_many(self):
        example_elements_json = [
            {
                '_id': '9c482525eaa14c3d808de7d1d1a483ep',
                '_value': 'EQObject'
            },
            {
                '_id': '9c482525eaa14c3d808de7d1d1a483eu',
                '_value': 'EQObject'
            }
        ]

        expected_result = {
            'acknowledged': True,
            'inserted_ids': [
                '9c482525eaa14c3d808de7d1d1a483ep',
                '9c482525eaa14c3d808de7d1d1a483eu'
            ]
        }

        loop = asyncio.get_event_loop()
        result_create = loop.run_until_complete(self.repository.create_many(elements=example_elements_json))
        self.assertIsInstance(result_create, dict)
        self.assertEqual(expected_result, result_create)

    def test_create_many_invalid_elements_type(self):
        example_elements_json = [
            123123,
            {
                '_id': '9c482525eaa14c3d808de7d1d1a483ju',
                '_value': 'EQObject'
            }
        ]

        expected_error_msg = 'elements not valid: must be list of dicts'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.create_many(elements=str(example_elements_json)))

        self.assertEqual(expected_error_msg, str(exc.exception))

    def test_create_many_invalid_elements_value(self):
        example_elements_json = [
            {
                '_id': '9c482525eaa14c3d808de7d1d1a483gf',
                '_value': 'EQObject'
            },
            {
                '_value': 'EQObject'
            }
        ]

        expected_error_msg = 'Missing key: \'_id\''

        with self.assertRaises(SchemaMissingKeyError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.create_many(elements=example_elements_json, validate=True))

        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_find(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}

        expected_result = [
            {
                '_id': '9c482525eaa14c3d808de7d1d1a483ew',
                '_value': 'EQObject'
            }
        ]

        loop = asyncio.get_event_loop()
        result_find = loop.run_until_complete(self.repository.find(query=query))
        self.assertIsInstance(result_find, list)
        self.assertEqual(expected_result, result_find)

    def test_findinvalid_query_type(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}

        expected_result = [
            {
                '_id': '9c482525eaa14c3d808de7d1d1a483ew',
                '_value': 'EQObject'
            }
        ]

        expected_error_msg = 'query not valid: must be dict'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.find(query=str(query)))
        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_update_one(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}
        update = {'$set': {'_value': 'EQObjectModified'}}

        expected_result = {
            'acknowledged': True,
            'modified_count': 1
        }

        loop = asyncio.get_event_loop()
        result_find = loop.run_until_complete(self.repository.update_one(query=query, update=update))
        self.assertIsInstance(result_find, dict)
        self.assertEqual(expected_result, result_find)

    def test_update_one_invalid_query_type(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}
        update = {'$set': {'_value': 'EQObjectModified'}}

        expected_error_msg = 'query must be dict'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.update_one(query=str(query), update=update))

        self.assertEqual(expected_error_msg, str(exc.exception))

    def test_update_one_invalid_update_type(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}
        update = {'$set': {'_value': 'EQObjectModified'}}

        expected_error_msg = 'update must be dict'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.update_one(query=query, update=str(update)))

        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_update_many(self):
        query = {'_value': 'EQObject'}
        update = {'$set': {'_value': 'EQObjectModified'}}

        expected_result = {
            'acknowledged': True,
            'modified_count': 2
        }

        loop = asyncio.get_event_loop()
        result_find = loop.run_until_complete(self.repository.update_many(query=query, update=update))
        self.assertIsInstance(result_find, dict)
        self.assertEqual(expected_result, result_find)

    def test_update_many_invalid_query_type(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}
        update = {'$set': {'_value': 'EQObjectModified'}}

        expected_error_msg = 'query must be dict'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.update_many(query=str(query), update=update))

        self.assertEqual(expected_error_msg, str(exc.exception))

    def test_update_one_invalid_update_type(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}
        update = {'$set': {'_value': 'EQObjectModified'}}

        expected_error_msg = 'update must be dict'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.update_many(query=query, update=str(update)))

        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_delete_one(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}

        expected_result = {
            'acknowledged': True,
            'deleted_count': 1
        }

        loop = asyncio.get_event_loop()
        result_find = loop.run_until_complete(self.repository.delete_one(query=query))
        self.assertIsInstance(result_find, dict)
        self.assertEqual(expected_result, result_find)

    @unittest.skip('Development test')
    def test_delete_one_no_documents(self):
        query = {'_id': 'none_id'}

        expected_result = {
            'acknowledged': True,
            'deleted_count': 0
        }

        loop = asyncio.get_event_loop()
        result_find = loop.run_until_complete(self.repository.delete_one(query=query))
        self.assertIsInstance(result_find, dict)
        self.assertEqual(expected_result, result_find)

    @unittest.skip('Development test')
    def test_update_one_invalid_query_type(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}

        expected_error_msg = 'query must be dict'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.delete_one(query=str(query)))

        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_update_one_more_than_one_document_found(self):
        query = {'_value': 'EQObjectModified'}

        expected_error_msg = 'Found more than one document: 2'

        with self.assertRaises(ValueError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.delete_one(query=query))

        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_delete_many(self):
        query = {'_value': 'EQObjectModified'}

        expected_result = {
            'acknowledged': True,
            'deleted_count': 2
        }

        loop = asyncio.get_event_loop()
        result_find = loop.run_until_complete(self.repository.delete_many(query=query))
        self.assertIsInstance(result_find, dict)
        self.assertEqual(expected_result, result_find)

    def test_delete_many_invalid_query_type(self):
        query = {'_id': '9c482525eaa14c3d808de7d1d1a483ew'}

        expected_error_msg = 'query must be dict'

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.repository.delete_many(query=str(query)))

        self.assertEqual(expected_error_msg, str(exc.exception))
