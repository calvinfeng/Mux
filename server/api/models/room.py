# Futures
from __future__ import unicode_literals

# Django
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the room")

    def __unicode__( self ):
        return self.name
