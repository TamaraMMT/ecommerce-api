from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    AttributeType,
    AttributeValue,
    ProductlineAttributeValue
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("alt_text", "order")


class AttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeType
        fields = ("name", "id")


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_type = AttributeTypeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = (
            "attribute_type",
            "attribute_value",
        )


class ProductlineAttributeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductlineAttributeValue
        fields = (
            "attribute_value",
            "productline",
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attr_values = {}
        for key in av_data:
            attr_values.update(
                {key["attribute_type"]["name"]: key["attribute_value"]}
            )
        data.update({"specification attributes": attr_values})

        return data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    product_line = ProductlineSerializer(many=True)
    product_type = serializers.CharField(source="product_type.name")

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
