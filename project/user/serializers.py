"""
Serializers user API
"""
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
            ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create user with encrypted password and return"""
        return get_user_model().objects.create_user(**validated_data)
