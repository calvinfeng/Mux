from channels.generic.websockets import JsonWebsocketConsumer, WebsocketDemultiplexer
from urlparse import parse_qs


class MessageJSONConsumer(JsonWebsocketConsumer):
    strict_ordering = False
    channel_session = True

    def connection_groups(self, **kwargs):
        """Called to return the list of groups to automatically add/remove this connection to/from.
        """
        if 'room_name' in kwargs:
            return [kwargs['room_name']]

        return ['lobby']

    def connect(self, message, **kwargs):
        """Perform things on connection start
        """
        params = parse_qs(message.content["query_string"])
        if 'room_name' in kwargs and 'username' in params:
            self.message.channel_session['username'] = params['username']
            self.message.channel_session["room"] = kwargs['room_name']
            self.message.reply_channel.send({"accept": True})
        else:
            self.message.reply_channel.send({"accept": False})

    def receive(self, content, **kwargs):
        """Called when a message is received with decoded JSON content
        """
        if 'message' in content:
            username = self.message.channel_session['username']
            room = self.message.channel_session['room']
            print 'Received message: %s from %s in %s' % (content['message'], username, room)

    def disconnect(self, message, **kwargs):
        """Perform things on connection close
        """
        if 'room_name' in kwargs:
            print 'Client has disconnected from %s' % kwargs['room_name']


class EchoJSONConsumer(JsonWebsocketConsumer):
    def connect(self, message, multiplexer, **kwargs):
        # Send data with the multiplexer
        multiplexer.send({'status': "I just connected!"})

    def disconnect(self, message, multiplexer, **kwargs):
        print ("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, multiplexer, **kwargs):
        # Simple echo
        multiplexer.send({"original_message": content})


class Demultiplexer(WebsocketDemultiplexer):
    """Write your JSON consumers here: {stream_name: consumer}"""
    consumers = {
        'echo': EchoJSONConsumer,
        'message': MessageJSONConsumer,
    }
