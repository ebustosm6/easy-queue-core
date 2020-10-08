from abc import ABC
from typing import List

from easyqueue.core.objects.base.eqshardedobject import EqShardedObject
from easyqueue.service.base_crud_service import BaseCRUDService
from easyqueue.core.response import ResponseDTO


class BaseCRUDShardedService(ABC):

    async def count(self, region: str, h3: str, query: dict = None) -> ResponseDTO:
        raise NotImplementedError()

    async def create_one(self, element: EqShardedObject) -> ResponseDTO:
        raise NotImplementedError()

    async def create_many(self, region: str, h3: str, elements: List[EqShardedObject]) -> ResponseDTO:
        raise NotImplementedError()

    async def find(self, region: str, h3: str, query: object = None) -> ResponseDTO:
        raise NotImplementedError()

    async def find_one(self, identificator: str, region: str, h3: str) -> ResponseDTO:
        raise NotImplementedError()

    async def update_one(self, identificator: str, region: str, h3: str, update: object) -> ResponseDTO:
        raise NotImplementedError()

    async def update_many(self, region: str, h3: str, update: object, query: object = None) -> ResponseDTO:
        raise NotImplementedError()

    async def delete_one(self, identificator: str, region: str, h3: str) -> ResponseDTO:
        raise NotImplementedError()

    async def delete_many(self, region: str, h3: str, query: object = None) -> ResponseDTO:
        raise NotImplementedError()
