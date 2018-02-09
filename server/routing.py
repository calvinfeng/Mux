from channels import route, route_class
from api.consumers import *

# route('http.request', http_consumer)
channel_routing = [
    route('websocket.connect', websocket_on_connect, path="^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route('websocket.receive', websocket_on_receive, path="^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route('websocket.disconnect', websocket_on_disconnect, path="^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route('message.save', message_on_save),
    route_class(MessageJSONConsumer, path="^/json/(?P<room_name>[a-zA-Z0-9_]+)/"),
    route_class(MessageDemultiplexer, path="^/demultiplex/(?P<room_name>[a-zA-Z0-9_]+)/"),
    route_class(EavesdropJSONConsumer, path="^/eavesdrop/(?P<room_name>[a-zA-Z0-9_]+)/")
]
