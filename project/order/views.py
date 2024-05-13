"""Views for Order API"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderItemSerializer


class OrderItemView(generics.ListAPIView):
    """List all order items for a specific order."""
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.orderitems.all()
