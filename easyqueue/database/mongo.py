from typing import Dict, List

from schema import Schema
from easyqueue.utils.validation import TypeValidator
from motor.motor_asyncio import AsyncIOMotorClient


class MongoRepository:

    uri: str = None
    database: str = None
    collection: str = None
    validation_schema: Schema = None

    def __init__(self, uri=None, database=None, collection=None, validation_schema=None):
        self.uri = uri if uri is not None else self.uri
        self.database = database if database is not None else self.database
        self.collection = collection if collection is not None else self.collection
        self.validation_schema = validation_schema if validation_schema is not None else self.validation_schema

        if self.uri is None or self.database is None:
            raise RuntimeError('Not possible to create MongoRepository, required class attributes: {req}'.format(
                req=', '.join(['uri', 'database'])
            ))
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(self.uri)[self.database]

    def __get_target_collection_or_raise(self, collection):
        target_collection = collection

        if collection is None:
            if self.collection is not None:
                target_collection = self.collection
            else:
                raise ValueError('Must set a default collection or pass colelction to method')
        else:
            if not isinstance(collection, str):
                raise TypeError('collection must be string, found {col}'.format(type(collection)))

        return target_collection

    def __validate(self, element: Dict, validate: bool):
        validated_element = element
        if validate:
            if self.validation_schema is None:
                raise ValueError('Must set calidation schema to use validate parameter')
            validated_element = self.validation_schema.validate(element)

        return validated_element

    async def count(self, query: Dict = {}, collection: str = None) -> Dict:
        TypeValidator.raise_validation_element_type(
            element_name='query', element=query, type_class=dict, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)
        num_documents = await self.client[target_collection].count_documents(query)
        result = dict(acknowledged=True, count=num_documents)
        return result

    async def create_one(self, element: Dict, collection: str = None, validate: bool = False) -> Dict:
        TypeValidator.raise_validation_element_type(
            element_name='element', element=element, type_class=dict, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)
        element = self.__validate(element, validate)
        mongo_result = await self.client[target_collection].insert_one(element)
        return dict(acknowledged=mongo_result.acknowledged, inserted_id=mongo_result.inserted_id)

    async def create_many(self, elements: List[Dict], collection: str = None, validate: bool = False) -> Dict:
        elements_ready = []

        TypeValidator.raise_validation_element_type(
            element_name='elements', element=elements, type_class=list, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)

        for element in elements:
            TypeValidator.raise_validation_element_type(
                element_name='element', element=element, type_class=dict, allow_none=False)

            element = self.__validate(element, validate)
            elements_ready.append(element)

        mongo_result = await self.client[target_collection].insert_many(elements_ready)
        return dict(acknowledged=mongo_result.acknowledged, inserted_ids=mongo_result.inserted_ids)

    async def find(self, query: Dict = {}, skip: int = None, limit: int = None, collection: str = None) -> List:
        TypeValidator.raise_validation_element_type(
            element_name='query', element=query, type_class=dict, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)

        if skip and limit:
            if not (isinstance(skip, int) and isinstance(limit, int) or skip < 0 or limit < 0):
                raise TypeError('skip and limit must be positive integers')
            if query is not None:
                cursor_result = self.client[target_collection].find(query).skip(skip).limit(limit)
            else:
                cursor_result = self.client[target_collection].find().skip(skip).limit(limit)

        elif skip and not limit:
            if not isinstance(skip, int) or skip < 0:
                raise ValueError('skip must be positive integer')
            if query is not None:
                cursor_result = self.client[target_collection].find(query).skip(skip)
            else:
                cursor_result = self.client[target_collection].find().skip(skip)

        elif limit and not skip:
            if not isinstance(limit, int) or limit < 0:
                raise ValueError('limit must be positive integer')
            if query is not None:
                cursor_result = self.client[target_collection].find(query).limit(limit)
            else:
                cursor_result = self.client[target_collection].find().limit(limit)

        else:
            if query is not None:
                cursor_result = self.client[target_collection].find(query)
            else:
                cursor_result = self.client[target_collection].find()

        return await cursor_result.to_list(None)

    async def find_one(self, query: Dict, collection: str = None) -> Dict:
        result = None
        TypeValidator.raise_validation_element_type(
            element_name='query', element=query, type_class=dict, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)
        num_documents = await self.client[target_collection].count_documents(query)
        if num_documents == 1:
            result = await self.client[target_collection].find_one(filter=query)  # {'$set': element}

        elif num_documents > 1:
            raise ValueError('Found more than one document: {num}'.format(num=num_documents))

        return result

    async def update_one(self, query: Dict, update: Dict, upsert: bool = True, collection: str = None):
        result = dict(acknowledged=True, deleted_count=0)
        TypeValidator.raise_validation_element_type(
            element_name='query', element=query, type_class=dict, allow_none=False)

        TypeValidator.raise_validation_element_type(
            element_name='update', element=update, type_class=dict, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)
        num_documents = await self.client[target_collection].count_documents(query)
        if num_documents == 1:
            mongo_result = await self.client[target_collection].update_one(
                filter=query, update=update, upsert=upsert)  # {'$set': element}
            result = dict(acknowledged=mongo_result.acknowledged, modified_count=mongo_result.modified_count)

        elif num_documents > 1:
            raise ValueError('Found more than one document: {num}'.format(num_documents))

        return result

    async def update_many(self, query: Dict, update: Dict, upsert: bool= True, collection: str = None):
        TypeValidator.raise_validation_element_type(
            element_name='query', element=query, type_class=dict, allow_none=False)

        TypeValidator.raise_validation_element_type(
            element_name='update', element=update, type_class=dict, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)
        mongo_result = await self.client[target_collection].update_many(
            filter=query, update=update, upsert=upsert)
        result = dict(acknowledged=mongo_result.acknowledged, modified_count=mongo_result.modified_count)

        return result

    async def delete_one(self, query: Dict, collection: str = None) -> Dict:
        result = dict(acknowledged=True, deleted_count=0)
        TypeValidator.raise_validation_element_type(
            element_name='query', element=query, type_class=dict, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)
        num_documents = await self.client[target_collection].count_documents(query)
        if num_documents == 1:
            mongo_result = await self.client[target_collection].delete_one(filter=query)  # {'$set': element}
            result = dict(acknowledged=mongo_result.acknowledged, deleted_count=mongo_result.deleted_count)

        elif num_documents > 1:
            raise ValueError('Found more than one document: {num}'.format(num=num_documents))

        return result

    async def delete_many(self, query: Dict, collection: str = None) -> Dict:
        TypeValidator.raise_validation_element_type(
            element_name='query', element=query, type_class=dict, allow_none=False)

        target_collection = self.__get_target_collection_or_raise(collection)
        mongo_result = await self.client[target_collection].delete_many(filter=query)
        result = dict(acknowledged=mongo_result.acknowledged, deleted_count=mongo_result.deleted_count)

        return result
