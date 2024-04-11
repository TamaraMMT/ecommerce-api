"""
Database models
"""
import os
import uuid
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from shortuuid.django_fields import ShortUUIDField


def productimage_image_file_path(instance, filename):
    """
    Generates a file path for a new productimage image.

    Args:
        instance: The ProductImage model instance.
        filename: The original filename of the uploaded image.

    Returns:
        A string representing the file path where the image will be saved.
    """
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'productimage', filename)


class IsActiveManager(models.Manager):
    """
    Manager class that filters the objects to only include active ones (is_active=True).

    Provides a method to easily retrieve active objects:

    ```python
    objects = IsActiveManager()
    ```
    """

    def active(self):
        return self.get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    class MPTTMeta:
        """Sorting order when inserting new child categories"""
        order_insertion_by = ["name"]

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    pid = ShortUUIDField(
        unique=True, length=8, max_length=10)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey("Category", on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    product_type = models.ForeignKey(
        "ProductType",
        on_delete=models.PROTECT,
        related_name="product_type_product"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    objects = IsActiveManager()

    def __str__(self):
        return str(self.name)


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=10, unique=True)
    stock_qty = models.PositiveIntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField()
    attributes = models.ManyToManyField(
        "Attribute",
        through="ProductlineAttributeValue",
        related_name="productline_attributes"
    )
    objects = IsActiveManager()

    class Meta:
        unique_together = ("product", "order")

    def __str__(self):
        return str(self.sku)


class ProductImage(models.Model):
    alt_text = models.CharField(max_length=100, null=False)
    url = models.ImageField(null=True, upload_to=productimage_image_file_path)
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = models.PositiveIntegerField(null=False)

    class Meta:
        unique_together = ("product_line", "order")

    def __str__(self):
        return str(self.alt_text)


class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Attribute(models.Model):
    """
    Represents an attribute associated with a product type,
    such as size, color, or material.
    """
    attribute_name = models.CharField(max_length=100)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="product_type_attributes"
    )

    def __str__(self):
        return f"{self.attribute_name}"

    class Meta:
        unique_together = ("attribute_name", "product_type")


class ProductlineAttributeValue(models.Model):
    """
    Represents the specific value of an attribute for a particular product line.
    """
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="productline_attributes_attr",

    )
    attribute_value = models.CharField(max_length=100)
    productline = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name="productline_attributes_pl",
    )

    def __str__(self):
        return f"{self.attribute}-{self.attribute_value}"

    class Meta:
        unique_together = ("attribute", "attribute_value", "productline")
