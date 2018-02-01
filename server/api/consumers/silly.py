from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
import json


def http_consumer(message):
    """A consumer that intercepts a http request"""
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])

    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


def websocket_on_connect(message):
    """Explicitly accept WebSocket connections by sending accept: True, otherwise it will stuck in handshaking process
    and the socket connection will never establish.
    """
    message.reply_channel.send({"accept": True})
    Group("chat").add(message.reply_channel)


def websocket_on_receive(message):
    """ASGI WebSocket packet-received and send-packet message types both have a text key for their textual data."""
    payload = {
        "text": message.content['text']
    }
    # message.reply_channel.send(payload)

    # Instead of sending to one person, now we are broadcasting to everyone who is part of the chat group.
    Group("chat").send(payload)


def websocket_on_disconnect(message):
    Group("chat").discard(message.reply_channel)
