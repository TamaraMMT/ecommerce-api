from django.contrib import admin
from product.models import (
    Category,
    Product,
    ProductLine,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('name', 'parent')


class ProductLineInline(admin.TabularInline):
    model = ProductLine

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]
    list_per_page = 10
    list_display = ('name', 'category', 'is_active')
    readonly_fields = ['pid']
