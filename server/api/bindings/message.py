from channels.binding.websockets import WebsocketBinding
from api.models import Message


class MessageBinding(WebsocketBinding):
    model = Message
    stream = 'message-stream'
    fields = ['__all__']

    @classmethod
    def group_names(cls, instance):
        """Returns a list of groups to send outbound updates to based on the instance
        """
        return ['message-update']

    def has_permission(self, user, action, pk):
        """Returns if an inbound binding update is allowed to actually be carried out on the model

        :param string action: Always one of the unicode strings 'create', 'update' or 'delete'
        """
        return True
