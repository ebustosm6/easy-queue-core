from easyqueue.core.objects.user.schema import UserSchema
from easyqueue.core.objects.base.eqobject import EQObject


class User(EQObject):

    __schema = UserSchema()
    __args = {'identificator', 'email', 'password', 'user_id'}
    __hash_args = {'email'}

    def __init__(self, identificator, email, password, region, is_active=True, image=None):
        self.email = email
        self.password = password
        self.region = region
        self.is_active = is_active
        self.image = image
        super().__init__(identificator=identificator)

    @classmethod
    def get_schema(cls):
        return cls.__schema

    @classmethod
    def get_args(cls):
        return cls.__args
