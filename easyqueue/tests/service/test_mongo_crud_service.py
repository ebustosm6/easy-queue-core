import unittest
import asyncio

from schema import Schema, And
from easyqueue.core.base import EQObject
from easyqueue.database.mongo import MongoRepository
from easyqueue.service.mongo_crud_service import MongoCRUDService


class TestMongoCRUDService(unittest.TestCase):

    def setUp(self):
        schema = Schema(
            {
                '_id': And(str, len),
                '_value': And(str, len)
            },
            ignore_extra_keys=False)
        repository = MongoRepository(
            uri='mongodb://localhost:27017/', database='test', collection='test', validation_schema=schema)
        self.service = MongoCRUDService(repository=repository)

    @unittest.skip('Development test')
    def test_create_one(self):
        example_element = EQObject()

        expected_result = {'acknowledged': True, 'inserted_id': example_element.id}

        loop = asyncio.get_event_loop()
        result_create = loop.run_until_complete(self.service.create_one(element=example_element))
        self.assertIsInstance(result_create, dict)
        self.assertEqual(expected_result, result_create)

    def test_create_one_invalid_element(self):
        expected_error_msg = 'Invalid type for {elem_name} with value {elem_val}, expected {exp_type}, found {f_type}' \
            .format(elem_name='element', elem_val=str(None), exp_type=EQObject,
                    f_type=type(None))

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.service.create_one(element=None))

        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_create_many(self):
        example_element_one = EQObject()
        example_element_two = EQObject()
        example_elements_json = [
            example_element_one, example_element_two
        ]

        expected_result = {
            'acknowledged': True,
            'inserted_ids': [
                example_element_one.id,
                example_element_two.id
            ]
        }

        loop = asyncio.get_event_loop()
        result_create = loop.run_until_complete(self.service.create_many(elements=example_elements_json))
        self.assertIsInstance(result_create, dict)
        self.assertEqual(expected_result, result_create)

    def test_create_many_invalid_elements_type(self):
        example_elements_json = [
            EQObject(), EQObject()
        ]

        expected_error_msg = 'Invalid type for {elem_name} with value {elem_val}, expected {exp_type}, found {f_type}' \
            .format(elem_name='elements', elem_val=str(example_elements_json), exp_type=list,
                    f_type=type(str(example_elements_json)))

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.service.create_many(elements=str(example_elements_json)))

        self.assertEqual(expected_error_msg, str(exc.exception))

    def test_create_many_invalid_elements_value(self):
        invalid_element = str(EQObject())
        example_elements_json = [
            invalid_element, EQObject()
        ]

        expected_error_msg = 'Invalid type for {elem_name} with value {elem_val}, expected {exp_type}, found {f_type}' \
            .format(elem_name='element', elem_val=invalid_element, exp_type=EQObject,
                    f_type=type(invalid_element))

        with self.assertRaises(TypeError) as exc:
            loop = asyncio.get_event_loop()
            _ = loop.run_until_complete(self.service.create_many(elements=example_elements_json))

        self.assertEqual(expected_error_msg, str(exc.exception))

    @unittest.skip('Development test')
    def test_find(self):
        example_element = EQObject()
        query = {'_id': example_element.id}

        expected_result = [
            example_element
        ]

        loop = asyncio.get_event_loop()
        _ = loop.run_until_complete(self.service.create_one(element=example_element))

        loop = asyncio.get_event_loop()
        result_find = loop.run_until_complete(self.service.find(query=query))
        self.assertIsInstance(result_find, list)
        self.assertEqual(expected_result, result_find)

    @unittest.skip('Development test')
    def test_find_one(self):
        example_element = EQObject()
        query = {'_id': example_element.id}

        expected_result = example_element

        loop = asyncio.get_event_loop()
        _ = loop.run_until_complete(self.service.create_one(element=example_element))

        loop = asyncio.get_event_loop()
        result_find = loop.run_until_complete(self.service.find_one(query=query))
        self.assertIsInstance(result_find, EQObject)
        self.assertEqual(expected_result, result_find)

# TODO: Complete remaining tests
