from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from product.models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    Attribute,
    ProductType,
    ProductAttributeValue
)


class ProductLineResource(resources.ModelResource):

    class Meta:
        model = ProductLine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('name', 'parent', 'slug', 'is_active')
    raw_id_fields = ['parent']


class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe(
                '<a class="button" href="{u}">Edit</a>&nbsp;'.format(u=url)
            )
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
    list_display = ('name', 'category', 'slug', 'is_active', 'product_type')
    readonly_fields = ['pid']
    raw_id_fields = ['product_type']


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['name']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["attribute_name", "product_type"]


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue


@admin.register(ProductLine)
class ProductLineAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProductLineResource]
    list_per_page = 10
    list_display = ("sku", "price", "stock_qty", "is_active", "product")
    inlines = [ProductImageInline, ProductAttributeValueInline]
    readonly_fields = ['product', 'order']

    def has_add_permission(self, request):
        return False


class ProductAttributeValueAdmin(admin.ModelAdmin):
    """
    Admin configuration for ProductlineAttributeValue model.
    """
    list_display = ("value", "attribute", "product_line", )
    readonly_fields = ("attribute", "value", "product_line")

    def has_add_permission(self, request):
        """
        Disallow adding ProductlineAttributeValue objects directly through the admin.
        """
        return False


admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
