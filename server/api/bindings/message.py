from channels.binding.websockets import WebsocketBinding
from channels import Group
from api.models import Message
import json


class MessageBinding(WebsocketBinding):
    model = Message
    stream = 'message-stream'
    fields = ['__all__']

    @classmethod
    def group_names(cls, instance):
        """Returns a list of groups to send outbound updates to based on the instance. Notice the instance is referring
        to the model instance that was modified. We can broadcast to different groups depending on which instance is
        modified using its id or name or whatever.

        :param Message cls: Message model class
        :param Message instance: An instance of Mesasge model class
        """
        return ['message-update']

    def has_permission(self, user, action, pk):
        """Returns if an inbound binding update is allowed to actually be carried out on the model

        :param string action: Always one of the unicode strings 'create', 'update' or 'delete'
        """
        return True

    def create(self, data):
        """Creates a new instance of the model with JSON data
        """
        print "Message model binding is trying to create instance with %s" % data
        Group('message-update').send({"text": json.dumps(data)})

    def update(self, pk, data):
        """Updates model with JSON data
        """
        print "Message model binding is trying to update model with %s" % data

    def delete(self, pk):
        """Deletes the model
        """
        print "Message model binding is trying to delete model with %s" % pk
