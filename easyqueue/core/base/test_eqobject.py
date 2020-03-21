import unittest
import copy
import random

from easyqueue.core.base import EQObject


class TestEQObject(unittest.TestCase):

    def setUp(self):
        random.seed(5432)
        self.example_eqobject_json = {
            "_id": "9c482525eaa14c3d808de7d1d1a483ed",
            "__type__": "EQObject",
            "_created_at": "2020-02-03T16:57:53.501633"
        }

        self.example_eqobject = EQObject()
        self.example_eqobject.__dict__ = copy.deepcopy(self.example_eqobject_json)

    def test_init(self):
        self.assertEqual(self.example_eqobject.id, self.example_eqobject_json["_id"])
        self.assertEqual(type(self.example_eqobject), EQObject)
        self.assertEqual(self.example_eqobject.created_at, self.example_eqobject_json["_created_at"])

    def test_id(self):
        self.assertEqual(self.example_eqobject_json['_id'], self.example_eqobject.id)

    def test_created_at(self):
        self.assertEqual(self.example_eqobject_json['_created_at'], self.example_eqobject.created_at)

    def test_json(self):
        self.assertEqual(self.example_eqobject_json, self.example_eqobject.json())

    def test_from_json(self):
        eq_object = EQObject.from_json(self.example_eqobject_json)
        self.assertEqual(eq_object.id, self.example_eqobject.id)
        self.assertEqual(type(eq_object), type(self.example_eqobject))
        self.assertEqual(eq_object.__type__, self.example_eqobject.__type__)
        self.assertEqual(eq_object.created_at, self.example_eqobject.created_at)

    def test_str(self):
        self.assertEqual(str(self.example_eqobject), str(self.example_eqobject.__dict__))

    def test_hash(self):
        self.assertEqual(hash(self.example_eqobject), hash(str(self.example_eqobject)))

    def test_eq(self):
        eq_obj = EQObject()
        eq_obj.__dict__ = copy.deepcopy(self.example_eqobject_json)
        self.assertTrue(self.example_eqobject == eq_obj)


if __name__ == '__main__':
    unittest.main()
