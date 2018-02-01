from channels import route
from api.consumers import http_consumer, ws_message


channel_routing = [
    # route('http.request', http_consumer),
    route('websocket.receive', ws_message)
]
