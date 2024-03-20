from factory.django import DjangoModelFactory
import factory
from product.models import (
    Category,
    Product,
    ProductLine,
    ProductImage
)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"test_category_{n}")
    slug = factory.Sequence(lambda n: f"test_slug_{n}")
    is_active = True


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


class ProductlineFactory(DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = factory.Sequence(lambda n:  f"{n:02d}")
    sku = factory.Sequence(lambda n: f"test_SKU_{n}")
    stock_qty = factory.Sequence(lambda n: f"0000_{n}")
    product = factory.SubFactory(ProductFactory)
    is_active = True
    order = factory.Sequence(lambda n: int(n))


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    alt_text = "test alternative text"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductlineFactory)
    order = factory.Sequence(lambda n: int(n))
