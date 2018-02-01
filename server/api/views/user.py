# Futures
from __future__ import unicode_literals

# Django
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response

# API
from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_field = ['username', 'first_name', 'last_name']
