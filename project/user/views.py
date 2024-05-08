"""
Views for the client API.
"""
from .serializers import UserProfileSerializer
from rest_framework import generics
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.response import Response


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View to retrieve and update user profile information."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        """Retrieve the currently authenticated user's profile."""
        user = self.request.user
        return user.userprofile

    def get(self, request, *args, **kwargs):
        """Retrieve the currently authenticated user's profile information."""
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """Update the currently authenticated user's profile information."""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
