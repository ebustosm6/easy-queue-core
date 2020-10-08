from easyqueue.core.objects.base.eqobject_schema import EQObjectSchema
from marshmallow import fields, ValidationError, validates


class EqShardedObjectSchema(EQObjectSchema):

    MIN_LIMIT = 0

    region = fields.Str(required=True)
    h3 = fields.Str(required=True)

    @validates('region')
    def validate_region(self, data: str):
        self.validate_non_empty(data=data)

    @validates('h3')
    def validate_h3(self, data: str):
        self.validate_non_empty(data=data)
