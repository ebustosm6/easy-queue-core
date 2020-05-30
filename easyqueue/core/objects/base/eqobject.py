import uuid
import json
from datetime import datetime

from easyqueue.core.objects.base.schema import EQObjectSchema


class EQObject:

    __schema = EQObjectSchema()
    __args = {'identificator'}
    __hash_args = {'identificator'}

    def __init__(self, identificator):
        self.identificator = identificator
        self.created_at = datetime.utcnow().timestamp()
        self.id = self._generate_id()
        self.validate()

    def __str__(self):
        return str(self.__dict__)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return all(
            isinstance(other, self.__class__),
            self.id == other.id
        )

    def validate(self):
        validation_errors = self.get_schema().validate(self.json())
        if validation_errors:
            raise ValueError(str(validation_errors))
        if self.id != self._generate_id():
            raise ValueError(str({'id': ['Invalid generated id']}))

    def _generate_id(self):
        hash_args = {self.__getattribute__(arg_name) for arg_name in self.__hash_args}
        hash_key = '{cls}({args})'.format(cls=self.__class__.__name__, args=','.join(hash_args))
        return uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=hash_key).hex

    @classmethod
    def get_schema(cls):
        return cls.__schema

    @classmethod
    def get_args(cls):
        return cls.__args

    def json(self, as_string=False):
        obj_json = self.__dict__
        if as_string:
            obj_json = json.dumps(self, sort_keys=True)

        return obj_json
    
    @classmethod
    def from_json(cls, obj, as_string=False):
        return_object = None
        input_init_args = {}

        if obj:
            obj_json = json.loads(obj) if as_string else obj
            validation_errors = cls.get_schema().validate(obj_json)
            if not validation_errors:
                init_args = __class__.get_args()
                for key, value in obj.items():
                    if key in init_args:
                        input_init_args[key] = value
                return_object = __class__(**input_init_args)
                return_object.__dict__ = obj_json
                return return_object
            else:
                raise ValueError(validation_errors)

        return return_object
