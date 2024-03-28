from django.db import models
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
from shortuuid.django_fields import ShortUUIDField 


class IsActiveManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)

    objects = IsActiveManager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    pid = ShortUUIDField(
        unique=True, length=8, max_length=10)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey("Category", on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_type"
    )
    objects = IsActiveManager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=10)
    stock_qty = models.PositiveIntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField()
    attribute_value = models.ManyToManyField(
        "AttributeValue",
        through="ProductlineAttributeValue",
        related_name="productline_attr_value",
    )
    objects = IsActiveManager()

    class Meta:
        unique_together = ("product", "order")

    def __str__(self):
        return str(self.sku)


class ProductImage(models.Model):
    alt_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = models.PositiveIntegerField(blank=True)

    class Meta:
        unique_together = ("product_line", "order")

    def __str__(self):
        return f"{self.product_line.sku}_img"


class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class AttributeType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product_type_attribute", default=1)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute_type = models.ForeignKey(
        AttributeType, on_delete=models.CASCADE, related_name="attribute_type_of_producttype"
    )

    def __str__(self):
        return f"{self.attribute_type.name}-{self.attribute_value}"

    class Meta:
        unique_together = ("attribute_value", "attribute_type")


class ProductlineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="productline_attr_value_av",
    )
    productline = models.ForeignKey(
        "ProductLine",
        on_delete=models.CASCADE,
        related_name="productline_attr_value_pl",
    )

    class Meta:
        unique_together = ("attribute_value", "productline")
