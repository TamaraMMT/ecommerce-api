from rest_framework import serializers


from .models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
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
        fields = ("alt_text", "order", "url")


class AttributeSerializer(serializers.ModelSerializer):
    attribute_type = serializers.CharField(source="attribute_name")

    class Meta:
        model = Attribute
        fields = ['attribute_type']


class ProductlineAttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = ProductlineAttributeValue
        fields = ['attribute', 'attribute_value']


class ProductlineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "is_active",
            "product_image",
            "attributes"
        )

    def get_attributes(self, obj):
        attributes = obj.productline_attributes_pl.prefetch_related('attribute')
        attr_data = []
        for attr_value in attributes:
            attr_data.append({
                attr_value.attribute.attribute_name: attr_value.attribute_value
            })
        return attr_data


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