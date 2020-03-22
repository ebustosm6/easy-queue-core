from typing import Dict, List

from easyqueue.core.base import EQObject


class BaseIEService:

    async def count(self, query: object) -> Dict:
        raise NotImplementedError()

    async def import_one(self, element: EQObject) -> Dict:
        raise NotImplementedError()

    async def import_many(self, elements: List[EQObject]) -> Dict:
        raise NotImplementedError()

    async def export_one(self, query: object) -> Dict:
        raise NotImplementedError()

    async def export_many(self) -> List[Dict]:
        raise NotImplementedError()
