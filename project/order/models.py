from django.db import models
from user.models import UserProfile
from product.models import ProductLine
from shortuuid.django_fields import ShortUUIDField


class Order(models.Model):
    number_order = ShortUUIDField(length=5, max_length=255, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        UserProfile, related_name='orders', on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
