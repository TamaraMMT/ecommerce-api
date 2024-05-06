"""
Views for the client API.
"""
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserProfileSerializer

from rest_framework.response import Response


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class UserProfileView(APIView):
    """View to retrieve and update user profile information."""
    # serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve the currently authenticated user."""
        return self.request.user

    def get(self, request):
        """Retrieve the currently authenticated user's profile information."""
        user = self.get_object()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
