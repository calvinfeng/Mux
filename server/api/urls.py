from __future__ import unicode_literals

# Django
from django.conf.urls import url, include
from django.views.generic.base import RedirectView

# REST
from rest_framework import routers

# API
from api.views import UserViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
