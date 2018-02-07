from channels.generic.websockets import WebsocketDemultiplexer
from api.bindings import MessageBinding


class MessageDemultiplexer(WebsocketDemultiplexer):
    """Notice that a binding has a .consumer attribute, which is a standard WebSocket JSON consumer, that the
    demultiplexer can pass demultiplexed websocket.receive message to.
    """
    consumers = {
        'message-stream': MessageBinding.consumer,
    }

    def connection_groups(self):
        """Returns a list of groups to put people in when they are connected as consumer
        """
        return ['message-update']
