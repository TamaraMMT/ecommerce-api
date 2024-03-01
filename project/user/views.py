"""
User API view
"""

from rest_framework import generics

from user.serializers import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    """Register new user"""
    serializer_class = UserSerializer
    