from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    AttributeType,
    AttributeValue
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["alt_text", "order"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_type = serializers.CharField(source="attribute_type.name")

    class Meta:
        model = AttributeValue
        fields = (
            "attribute_type",
            "attribute_value",
        )


class ProductlineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "is_active",
            "product_image",
            "attribute_value"
        )


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    product_line = ProductlineSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "category",
            "product_line",
        )
