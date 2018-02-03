from channels.generic.websockets import JsonWebsocketConsumer
from urlparse import parse_qs
import pdb


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
