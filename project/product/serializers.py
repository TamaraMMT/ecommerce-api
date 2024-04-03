from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    ProductType,
    Attribute,
    ProductlineAttributeValue,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("alt_text", "order")


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("attribute_name", "product_type")


class ProductlineAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductlineAttributeValue

        fields = ("attribute_value", "productline")


class ProductlineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attributes = AttributeSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "is_active",
            "product_image",
            "attributes",
        )


class ProductSerializer(serializers.ModelSerializer):
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