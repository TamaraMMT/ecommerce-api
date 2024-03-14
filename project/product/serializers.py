from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductLine
)



class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "category_name",
        )



class ProductlineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "product_name",
        )
