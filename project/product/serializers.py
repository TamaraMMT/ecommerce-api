from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductLine,
    ProductImage
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["alt_text", "order"]


class ProductlineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "is_active",
            "product_image"
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
            "product_line"
        )
