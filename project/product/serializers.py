"""
Serializer for products APIs
"""

from rest_framework import serializers


from .models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    ProductAttributeValue,
)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Categories"""

    class Meta:
        model = Category
        fields = ["name"]


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for Product Images"""

    class Meta:
        model = ProductImage
        fields = ("alt_text", "order", "url")


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for Product Attribute Values"""
    attribute_name = serializers.CharField(
        source='attribute.attribute_name', read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ['attribute_name', 'value']


class ProductlineSerializer(serializers.ModelSerializer):
    """Serializer for Product Lines"""
    product_image = ProductImageSerializer(many=True)
    product_line_attributes = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "is_active",
            "product_image",
            "product_line_attributes"
        )


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Products"""
    category = serializers.CharField(source="category.name")
    product_type = serializers.CharField(source="product_type.name")
    product_line = ProductlineSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "category",
            "product_type",
            "product_line",
        )
