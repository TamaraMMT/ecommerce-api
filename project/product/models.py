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
    slug = models.SlugField(max_length=255, unique=True)
    pid = ShortUUIDField(
        unique=True, length=8, max_length=10)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey("Category", on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_type_product"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    objects = IsActiveManager()

    class Meta:
        unique_together = ("name", "slug")


    def __str__(self):
        return self.name


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
        "Attribute", through="ProductlineAttributeValue", related_name="productline_attributes"
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


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=100)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product_type_attributes"
    )

    def __str__(self):
        return f"{self.product_type}-{self.attribute_name}"

    class Meta:
        unique_together = ("attribute_name", "product_type")


class ProductlineAttributeValue(models.Model):
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
