from easyqueue.core.objects.base.eqshardedobject import EqShardedObject
from easyqueue.core.objects.queue.queue_schema import QueueSchema
from easyqueue.core.objects.base.eqobject import EQObject


class Queue(EqShardedObject):

    USER_ID = 'user_id'

    _schema = QueueSchema()
    _args = {EQObject.IDENTIFICATOR, EqShardedObject.REGION, EqShardedObject.H3, USER_ID}
    _hash_args = {EQObject.IDENTIFICATOR, EqShardedObject.REGION, USER_ID}

    def __init__(self, identificator, region, h3, user_id, group='default', info='', tags=set(), limit=0,
                 is_active=True, image=None):
        self.user_id = user_id
        self.group = group
        self.info = info
        self.tags = tags
        self.limit = limit
        self.is_active = is_active
        self.image = image
        super().__init__(identificator=identificator, region=region, h3=h3)
