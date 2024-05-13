from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import OrderItem, Order


class OrderSerializer(ModelSerializer):
    """Serializer for the user profile."""
    user = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'number_order',
            'user',
        ]


class OrderItemSerializer(ModelSerializer):
    """Serializer for the user profile."""
    order = OrderSerializer(read_only=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='product.productline.price', read_only=True)
    product = serializers.CharField(
        source='product.product.name', read_only=True)

    class Meta:
        model = OrderItem

        fields = [
            'order',
            'product',
            'quantity',
            'price',
        ]
