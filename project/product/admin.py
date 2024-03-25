from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from product.models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    AttributeValue,
    AttributeType,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('name', 'parent', 'slug', 'is_active')


class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe('<a class="button" href="{u}">Edit</a>&nbsp;'.format(u=url))
            return link
        else:
            return ""


class ProductLineInline(EditLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]
    list_per_page = 10
    list_display = ('name', 'category', 'slug', 'is_active')
    readonly_fields = ['pid']


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue.productline_attr_value.through


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('sku', 'price', 'stock_qty', 'is_active', 'product')
    inlines = [ProductImageInline, AttributeValueInline]


admin.site.register(AttributeType)
admin.site.register(AttributeValue)
