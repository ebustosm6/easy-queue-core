from easyqueue.core.objects.queue.schema import QueueSchema
from easyqueue.core.objects.base.eqobject import EQObject


class Queue(EQObject):

    REGION = 'region'
    USER_ID = 'user_id'
    GROUP = 'group'
    INFO = 'info'
    TAGS = 'tags'
    LIMIT = 'limit'
    IS_ACTIVE = 'is_active'
    IMAGE = 'image'

    _schema = QueueSchema()
    _args = {EQObject.IDENTIFICATOR, REGION, USER_ID}
    _hash_args = {EQObject.IDENTIFICATOR, REGION, USER_ID}

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
