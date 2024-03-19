from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from shortuuid.django_fields import ShortUUIDField 



class Category(MPTTModel):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True
    )
    is_active = models.BooleanField(default=False)

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

    class Meta:
        unique_together = ("product", "order")

    def __str__(self):
        return str(self.sku)
