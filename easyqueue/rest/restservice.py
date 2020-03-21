import json
import dateutil.parser

from schema import Schema, And, Or
from easyqueue.core.base import EQObject


schema = Schema({
    '_id': And(str, len),
    '_created_at': And(str, lambda n: dateutil.parser.parse(n)),
    '__type__': 'RestService',
    '_host': And(str, len),
    '_port': Or(None, int),
    '_context_path': And(str, len)}, ignore_extra_keys=True)


class EQDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(obj):
        res = None
        
        if '__type__' in obj and '_host' in obj and obj['__type__'] == 'RestService':
            o = RestService(host=obj['_host'])
            o.__dict__ = obj
            res = o
        
        return res


class RestService(EQObject):

    def __init__(self, host, port=None, context_path='/'):
        super().__init__()
        assert host is not None, 'Host can not be None'

        self._host = str(host)
        self._port = int(port) if port is not None else port
        self._context_path = str(context_path) if str(context_path).startswith('/') else '/{cp}'.format(cp=context_path)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def context_path(self):
        return self._context_path

    @property
    def hostport(self):
        return '{host}:{port}'.format(host=self.host, port=self.port) if self.port is not None else self.host

    @property
    def uri(self):
        return '{hp}{cp}'.format(hp=self.hostport, cp=self.context_path)

    @staticmethod
    def from_json(obj):
        return EQDecoder().object_hook(schema.validate(obj))
