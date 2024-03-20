from django.db import models

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

    objects = IsActiveManager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=10)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField()

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
