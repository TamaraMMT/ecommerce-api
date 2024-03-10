from rest_framework import serializers

from .models import (
    Category,
    Product,
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
