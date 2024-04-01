from factory.django import DjangoModelFactory
import factory
from product.models import (
    AttributeType,
    AttributeValue,
    Category,
    Product,
    ProductLine,
    ProductImage,
    ProductType,
    ProductlineAttributeValue,
)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"test_category_{n}")
    slug = factory.Sequence(lambda n: f"test_slug_{n}")
    is_active = True


class ProductTypeFactory(DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: f"test_product_type_{n}")


class AttributeTypeFactory(DjangoModelFactory):
    class Meta:
        model = AttributeType

    name = factory.Sequence(lambda n: f"test_name_attr_{n}")
    description = factory.Sequence(lambda n: f"attr_description_{n}")
    product_type = factory.SubFactory(ProductTypeFactory)


class AttributeValueFactory(DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = factory.Sequence(lambda n: f"test_name_attr_{n}")
    attribute_type = factory.SubFactory(AttributeTypeFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"test_category_{n}")
    slug = factory.Sequence(lambda n: f"test_slug_{n}")
    pid = factory.Sequence(lambda n: f"0000_{n}")
    description = "test_description"
    is_digital = False
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductlineFactory(DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = factory.Sequence(lambda n:  f"{n:02d}")
    sku = factory.Sequence(lambda n: f"test_SKU_{n}")
    stock_qty = factory.Sequence(lambda n: f"0000_{n}")
    product = factory.SubFactory(ProductFactory)
    is_active = True
    order = factory.Sequence(lambda n: int(n))
    attribute_value = factory.RelatedFactory(AttributeValueFactory, 'attribute_type')


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    alt_text = "test alternative text"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductlineFactory)
    order = factory.Sequence(lambda n: int(n))


class ProductlineAttributeValueFactory(DjangoModelFactory):
    class Meta:
        model = ProductlineAttributeValue
    
    attribute_value = factory.SubFactory(AttributeValueFactory)
    productline = factory.SubFactory(ProductlineFactory)
