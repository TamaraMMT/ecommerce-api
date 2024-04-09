from factory.django import DjangoModelFactory
import factory
from product.models import (
    Attribute,
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


class AttributeFactory(DjangoModelFactory):
    class Meta:
        model = Attribute

    attribute_name = factory.Sequence(lambda n: f"test_name_attr_{n}")
    product_type = factory.SubFactory(ProductTypeFactory)



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
    sku = factory.Sequence(lambda n: f"SKU_{n}")
    stock_qty = factory.Sequence(lambda n: f"0000_{n}")
    product = factory.SubFactory(ProductFactory)
    is_active = True
    order = factory.Sequence(lambda n: int(n))
    attributes = factory.RelatedFactory(AttributeFactory)


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    alt_text = factory.Sequence(lambda n: f"test alternative text {n}")
    url = factory.LazyAttribute(lambda o: f"{o.alt_text}.jpg")
    productline = factory.RelatedFactory(ProductlineFactory)
    order = factory.Sequence(lambda n: int(n))


class ProductlineAttributeValueFactory(DjangoModelFactory):
    class Meta:
        model = ProductlineAttributeValue

    attribute_value = factory.Sequence(lambda n: f"test_name_attr_value{n}")
    attribute = factory.SubFactory(AttributeFactory)
    productline = factory.SubFactory(ProductlineFactory)
