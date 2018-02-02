from channels import route
from api.consumers import *

# route('http.request', http_consumer)
channel_routing = [
    route('websocket.connect', websocket_on_connect, path="^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route('websocket.receive', websocket_on_receive, path="^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route('websocket.disconnect', websocket_on_disconnect, path="^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route('message.save', message_on_save)
]
