from easyqueue.core.objects.queue.schema import QueueSchema
from easyqueue.core.objects.base.eqobject import EQObject


class Queue(EQObject):

    __schema = QueueSchema()
    __args = {'identificator', 'user_id'}
    __hash_args = {'identificator', 'region', 'user_id'}

    def __init__(self, identificator, region, user_id, group='default', info='', tags=set(), limit=0,
                 is_active=True, image=None):
        self.user_id = user_id
        self.region = region
        self.group = group
        self.info = info
        self.tags = tags
        self.limit = limit
        self.is_active = is_active
        self.image = image
        super().__init__(identificator=identificator)

    @classmethod
    def get_schema(cls):
        return cls.__schema

    @classmethod
    def get_args(cls):
        return cls.__args
