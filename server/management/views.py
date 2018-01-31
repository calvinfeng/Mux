from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Renders a management single page application.
    """
    template_name = 'management.html'
