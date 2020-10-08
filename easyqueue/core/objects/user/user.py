from easyqueue.core.objects.base.eqshardedobject import EqShardedObject

from easyqueue.core.objects.user.user_schema import UserSchema


class User(EqShardedObject):

    EMAIL = 'email'
    PASSWORD = 'password'
    REGION = 'region'

    _schema = UserSchema()
    _args = {EqShardedObject.IDENTIFICATOR, EqShardedObject.REGION, EqShardedObject.H3, EMAIL, PASSWORD}
    _hash_args = {EqShardedObject.IDENTIFICATOR}

    def __init__(self, identificator, email, password, region, h3, is_active=True, image=None):
        self.email = email
        self.password = password
        self.is_active = is_active
        self.image = image
        super().__init__(identificator=identificator, region=region, h3=h3)
