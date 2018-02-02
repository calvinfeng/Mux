# Futures
from __future__ import unicode_literals

# Django
from rest_framework import viewsets, status
from rest_framework.response import Response

# API
from api.serializers import MessageSerializer
from api.models import Message

class MessageViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    search_field = ['author', 'body', 'room']
