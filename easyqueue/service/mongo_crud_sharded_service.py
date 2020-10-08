from typing import Dict, List, Type

from easyqueue.core.objects.base.eqshardedobject import EqShardedObject

from easyqueue.core.response import ResponseDTO
from easyqueue.utils.validation import TypeValidator
from easyqueue.core.objects.base.eqobject import EQObject
from easyqueue.database.mongo.repository import MongoRepository
from service.base_crud_sharded_service import BaseCRUDShardedService


class MongoCRUDShardedService(BaseCRUDShardedService):

    repository: MongoRepository = None
    base_object_class: Type = EqShardedObject

    def __init__(self, repository: MongoRepository = None, base_object_class: Type = None) -> None:
        self.repository = repository if repository is not None else self.repository
        self.base_object_class = base_object_class if base_object_class is not None else self.base_object_class

    @classmethod
    def __get_validated_element(cls, element: EqShardedObject, allow_none: bool = False) -> Dict:
        validated_object = None
        if isinstance(element, cls.base_object_class):
            validated_object = element.json()
        else:
            TypeValidator.raise_validation_element_type(
                element_name='element', element=element, type_class=EQObject, allow_none=allow_none)

        return validated_object

    @classmethod
    def __handle_query(cls, identificator: str, region: str, h3: str, query: Dict) -> Dict:
        if not isinstance(query, dict):
            query = {}
        if identificator:
            query['identificator'] = identificator
        if region:
            query['region'] = region
        if h3:
            query['h3'] = h3
        return query

    @classmethod
    def __validate_sharded(cls, identificator, region, h3):
        if identificator:
            TypeValidator.raise_validation_element_empty_and_type(
                element_name='identificator', element=identificator, type_class=str, allow_none=False)
        if region:
            TypeValidator.raise_validation_element_empty_and_type(
                element_name='region', element=region, type_class=str, allow_none=False)
        if h3:
            TypeValidator.raise_validation_element_empty_and_type(
                element_name='h3', element=h3, type_class=str, allow_none=False)

    async def count(self, region: str, h3: str, query: Dict = None) -> ResponseDTO:
        self.__validate_sharded(region=region, h3=h3)
        query = self.__handle_query(region=region, h3=h3, query=query)
        return await self.repository.count(query=query)

    async def create_one(self, element: EqShardedObject) -> ResponseDTO:
        return await self.repository.create_one(element=self.__get_validated_element(element))

    async def create_many(self, region: str, h3: str, elements: List[EqShardedObject]) -> ResponseDTO:
        TypeValidator.raise_validation_element_type(
            element_name='elements', element=elements, type_class=list, allow_none=False)
        self.__validate_sharded(region=region, h3=h3)
        validated_elements = []
        for element in elements:
            validated_elements.append(self.__get_validated_element(element))
        return await self.repository.create_many(elements=validated_elements)

    async def find_one(self, identificator: str, region: str, h3: str) -> ResponseDTO:
        self.__validate_sharded(identificator=identificator, region=region, h3=h3)
        query = self.__handle_query(identificator=identificator, region=region, h3=h3, query=None)
        response_result = await self.repository.find_one(query=query)
        data_result = self.base_object_class.from_json(response_result.data)
        response_result_parsed = ResponseDTO(code=response_result.code, data=data_result)
        return response_result_parsed

    async def find_many(self, region: str, h3: str, query: Dict = None, skip: int = 0, limit: int = 0) -> ResponseDTO:
        self.__validate_sharded(region=region, h3=h3)
        query = self.__handle_query(region=region, h3=h3, query=query)
        response_result = await self.repository.find(query=query, skip=skip, limit=limit)
        raw_results = response_result.data
        parsed_results = []
        for raw_result in raw_results:
            parsed_results.append(self.base_object_class.from_json(raw_result))
        response_result_parsed = ResponseDTO(code=response_result.code, data=parsed_results)
        return response_result_parsed

    async def update_one(self, identificator: str, region: str, h3: str, update: EqShardedObject) -> ResponseDTO:
        self.__validate_sharded(identificator=identificator, region=region, h3=h3)
        TypeValidator.raise_validation_element_type(
            element_name='update', element=update, type_class=dict, allow_none=False)
        query = self.__handle_query(identificator=identificator, region=region, h3=h3, query=None)
        update_json = update.json(as_string=False)
        return await self.repository.update_one(query=query, update=update_json)

    async def update_many(self, region: str, h3: str, update: Dict, query: Dict = None) -> ResponseDTO:
        self.__validate_sharded(region=region, h3=h3)
        TypeValidator.raise_validation_element_type(
            element_name='update', element=update, type_class=dict, allow_none=False)
        query = self.__handle_query(region=region, h3=h3, query=query)
        return await self.repository.update_many(query=query, update=update)

    async def delete_one(self, identificator: str, region: str, h3: str) -> ResponseDTO:
        self.__validate_sharded(identificator=identificator, region=region, h3=h3)
        query = self.__handle_query(identificator=identificator, region=region, h3=h3, query=None)
        return await self.repository.delete_one(query=query)

    async def delete_many(self, region: str, h3: str, query: Dict = None) -> ResponseDTO:
        self.__validate_sharded(region=region, h3=h3)
        query = self.__handle_query(region=region, h3=h3, query=query)
        return await self.repository.delete_many(query=query)
