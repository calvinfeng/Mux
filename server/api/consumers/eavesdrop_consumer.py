from channels.generic.websockets import JsonWebsocketConsumer, WebsocketDemultiplexer
from urlparse import parse_qs


class EavesdropJSONConsumer(JsonWebsocketConsumer):
    strict_ordering = False
    channel_sesion = True

    def connection_groups(self, **kwargs):
        return ['message-update']

    def connect(self, message, **kwargs):
        """Called when client is connected
        """
        self.message.reply_channel.send({"accept": True})

    def receive(self, content, **kwargs):
        """Called when a message is received
        """
        print 'Eavedropping: got a message! %s' % content

    def disconnect(self, content, **kwargs):
        """Called when connection is closed
        """
        print 'Client has disconnected.'
