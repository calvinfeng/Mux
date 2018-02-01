# Futures
from __future__ import unicode_literals

# Django
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    author = models.ForeignKey(User,
                               db_index=True,
                               related_name='messages',
                               on_delete=models.CASCADE,
                               help_text="Message that belongs to a user")

    body = models.CharField(max_length=500,
                            help_text="Content of the message")
