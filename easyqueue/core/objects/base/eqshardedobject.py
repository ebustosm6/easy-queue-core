from easyqueue.core.objects.base.eqshardedobject_schema import EqShardedObjectSchema
from easyqueue.core.objects.base.eqobject import EQObject


class EqShardedObject(EQObject):

    REGION = 'region'
    H3 = 'h3'

    _schema = EqShardedObjectSchema()
    _args = {EQObject.IDENTIFICATOR, REGION, H3}
    _hash_args = {EQObject.IDENTIFICATOR}

    def __init__(self, identificator, region, h3):
        self.region = region
        self.h3 = h3
        super().__init__(identificator=identificator)
