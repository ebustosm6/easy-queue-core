from typing import Dict, List

from easyqueue.core.base import EQObject


class BaseCRUDService:

    async def count(self, query: dict) -> Dict:
        raise NotImplementedError()

    async def create_one(self, element: EQObject) -> Dict:
        raise NotImplementedError()

    async def create_many(self, elements: List[EQObject]) -> Dict:
        raise NotImplementedError()

    async def find(self, query: object) -> List[EQObject]:
        raise NotImplementedError()

    async def find_one(self, query: object) -> EQObject:
        raise NotImplementedError()

    async def update_one(self, query: object, update: object) -> Dict:
        raise NotImplementedError()

    async def update_many(self, query: object, update: object) -> Dict:
        raise NotImplementedError()

    async def delete_one(self, query: object) -> Dict:
        raise NotImplementedError()

    async def delete_many(self, query: object) -> Dict:
        raise NotImplementedError()
