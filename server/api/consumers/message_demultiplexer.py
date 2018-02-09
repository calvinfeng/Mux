from channels.generic.websockets import WebsocketDemultiplexer
from api.bindings import MessageBinding


class MessageDemultiplexer(WebsocketDemultiplexer):
    """Notice that a binding has a .consumer attribute, which is a standard WebSocket JSON consumer, that the
    demultiplexer can pass demultiplexed websocket.receive message to.
    """
    consumers = {
        'message-stream': MessageBinding.consumer,
    }

    def connection_groups(self, **kwargs):
        """Returns a list of groups to put people in when they are connected as consumer
        """
        print "Client is hitting Message demultiplexer with following kwargs: %s" % kwargs
        return ['message-update']

    def receive(self, content, **kwargs):
        print 'Message demultiplexer is receiving: %s' % content
        super(MessageDemultiplexer, self).receive(content, **kwargs)
