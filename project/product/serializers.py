from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductLine
)


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category"]


class ProductlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "is_active"
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
