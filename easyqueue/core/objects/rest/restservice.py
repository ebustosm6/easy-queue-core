from easyqueue.core.objects.rest.schema import RestServiceSchema
from easyqueue.core.objects.base.eqobject import EQObject


class RestService(EQObject):

    __schema = RestServiceSchema()
    __args = {'identificator', 'host'}
    __hash_args = {'host', 'context_path'}

    def __init__(self, identificator, host, port=None, context_path='/'):
        self.host = str(host)
        self.port = int(port) if port is not None else port
        self.context_path = str(context_path) if str(context_path).startswith('/') else '/{cp}'.format(cp=context_path)
        super().__init__(identificator=identificator)

    @property
    def hostport(self):
        return '{host}:{port}'.format(host=self.host, port=self.port) if self.port is not None else self.host

    @property
    def uri(self):
        return '{hp}{cp}'.format(hp=self.hostport, cp=self.context_path)

    @classmethod
    def get_schema(cls):
        return cls.__schema

    @classmethod
    def get_args(cls):
        return cls.__args
