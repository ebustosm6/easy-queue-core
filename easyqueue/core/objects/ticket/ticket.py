from easyqueue.core.objects.base.eqshardedobject import EqShardedObject

from easyqueue.core.objects.ticket.ticket_schema import TicketSchema
from easyqueue.core.objects.base.eqobject import EQObject


class Ticket(EqShardedObject):

    TICKET = 'ticket'
    USER_ID = 'user_id'
    USER_IDENTIFICATOR = 'user_identificator'
    REGION = 'region'
    QUEUE_ID = 'queue_id'
    QUEUE_IDENTIFICATOR = 'queue_identificator'

    _schema = TicketSchema()
    _args = {EqShardedObject.REGION, EqShardedObject.H3, USER_ID, USER_IDENTIFICATOR, REGION, QUEUE_ID, QUEUE_IDENTIFICATOR}
    _hash_args = {EQObject.IDENTIFICATOR, EqShardedObject.REGION, USER_ID, QUEUE_ID}

    def __generate_identificator(self, region, h3, user_identificator, queue_identificator):
        return '{ticket}_{region}_{h3}_{user}_{queue}'.format(
            ticket=self.TICKET, region=region, h3=h3, user=user_identificator, queue=queue_identificator)

    def __init__(self,  user_id, user_identificator, region, h3, queue_id, queue_identificator, is_active=True):
        self.user_id = user_id
        self.user_identificator = user_identificator
        self.queue_id = queue_id
        self.queue_identificator = queue_identificator
        self.is_active = is_active
        super().__init__(
            identificator=self.__generate_identificator(
                region=region, h3=h3, user_identificator=user_identificator, queue_identificator=queue_identificator),
            region=region,
            h3=h3
        )
