from channels import route
from api.consumers import http_consumer, websocket_on_receive, websocket_on_connect, websocket_on_disconnect

# route('http.request', http_consumer)
channel_routing = [
    route('websocket.connect', websocket_on_connect),
    route('websocket.receive', websocket_on_receive),
    route('websocket.disconnect', websocket_on_disconnect)
]
