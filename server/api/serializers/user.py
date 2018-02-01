# Futures
from __future__ import unicode_literals

# Django
from django.db import transaction
from django.core import exceptions
from django.contrib.auth.models import User
from rest_framework import serializers, fields


class UserSerializer(serializers.ModelSerializer):
    """Default JSON serializer for users when doing CRUD"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        """Overriding default validate method"""
        email = data['email']
        user_query_set = User.objects.filter(email=email)
        if user_query_set.exists():
            raise exceptions.ValidationError("This user has already registered.")

        return data

    def validate_password(self, field_value):
        """Overriding default field validation method"""
        if len(field_value) < 8:
            raise exceptions.ValidationError("Password is too short.")

        return field_value

    @transaction.atomic
    def create(self, validated_data):
        """Overriding default create method"""
        new_user = User(username=validated_data['username'], email=validated_data['email'])
        new_user.set_password(validated_data['password'])
        new_user.save()

        return new_user
