# Futures
from __future__ import unicode_literals

# Django
from django.db import transaction
from django.core import exceptions
from rest_framework import serializers, fields

# API
from api.models import Message

class MessageSerializer(serializers.ModelSerializer):
    """Default JSON serializer for messages when doing CRUD"""

    class Meta:
        model = Message
        fields = ['id', 'author', 'body']
