"""
Serializers for the client API View.
"""
from typing_extensions import ReadOnly
from django.utils.translation import gettext as _
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from user.models import UserProfile


class UserSerializer(ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password',]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserProfileSerializer(ModelSerializer):
    """Serializer for the user profile."""
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'shipping_address',
            'billing_address'
        ]
