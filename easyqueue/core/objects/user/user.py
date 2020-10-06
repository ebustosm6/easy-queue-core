from easyqueue.core.objects.user.schema import UserSchema
from easyqueue.core.objects.base.eqobject import EQObject


class User(EQObject):

    EMAIL = 'email'
    PASSWORD = 'password'
    REGION = 'region'
    IS_ACTIVE = 'is_active'
    IMAGE = 'image'

    _schema = UserSchema()
    _args = {EQObject.IDENTIFICATOR, EMAIL, PASSWORD, REGION}
    _hash_args = {EQObject.IDENTIFICATOR}

    def __init__(self, identificator, email, password, region, is_active=True, image=None):
        self.email = email
        self.password = password
        self.region = region
        self.is_active = is_active
        self.image = image
        super().__init__(identificator=identificator)
