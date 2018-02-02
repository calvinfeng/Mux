# Futures
from __future__ import unicode_literals

# Django
from rest_framework import authentication
from django.contrib.auth.models import User

class AuthenticationClass(authentication.BaseAuthentication):
    def __init__(self):
        super(AuthenticationClass, self).__init__()

    def authenticate(self, request):
        token = '1234'
        try:
            user = User.objects.get(username='calvinfeng')
        except User.DoesNotExist:
            return (None, None)
            
        return (user, token)

    def authenticate_header(self, request):
        return 'Token'
