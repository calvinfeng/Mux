from django.conf.urls import url
from django.views.generic.base import RedirectView
from management.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]
