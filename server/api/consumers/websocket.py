import json
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Channel, Group
from channels.sessions import channel_session
from api.models import Room, Message
from django.contrib.auth.models import User
from channels.auth import channel_session_user, channel_session_user_from_http
from urlparse import parse_qs


def http_consumer(message):
    """A consumer that intercepts a http request"""
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])

    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


@channel_session
def websocket_on_connect(message, room_name):
    """Explicitly accept WebSocket connections by sending accept: True, otherwise it will stuck in handshaking process
    and the socket connection will never establish.
    """
    message.reply_channel.send({"accept": True})

    params = parse_qs(message.content["query_string"])
    if b"username" in params:
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        message.channel_session["room"] = room_name
        Group("chat-room-%s" % room_name).add(message.reply_channel)
    else:
        message.reply_channel.send({"close": True})


@channel_session
def websocket_on_receive(message, room_name):
    """ASGI WebSocket packet-received and send-packet message types both have a text key for their textual data."""
    # Instead of sending to one person, now we are broadcasting to everyone who is part of the chat group.
    Group("chat-room-%s" % room_name).send({
        "text": json.dumps({
            "text": message["text"],
            "username": message.channel_session["username"],
            "room": message.channel_session["room"]
        })
    })
    # message.reply_channel.send(payload)

    # Sending a dict to channel
    Channel("message.save").send({
        "text": message["text"],
        "username": message.channel_session["username"],
        "room": message.channel_session["room"]
    })


@channel_session
def websocket_on_disconnect(message, room_name):
    Group("chat-room-%s" % room_name).discard(message.reply_channel)


def message_on_save(message):
    try:
        room = Room.objects.get(name=message.content['room'])
    except Room.DoesNotExist:
        room = Room.objects.create(name=message.content['room'])
    
    try:
        user = User.objects.get(username=message.content['username'])
    except User.DoesNotExist:
        return

    message = Message(author=user, room=room, body=message.content['text'])
    message.save()
    print "Saving message: %s from %s for room %s" % (message.body, message.author.username, message.room.name)
