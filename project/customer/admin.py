
from django.contrib import admin
from customer.models import Customer, Profile


@admin.register(Customer)
class CustomerUser(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('email', 'is_active')
    readonly_fields = ['last_login', 'pid']


@admin.register(Profile)
class ProfileCustomer(admin.ModelAdmin):
    ordering = 'firstname',
    list_per_page = 10
    list_display = ('customeruser', 'firstname', 'lastname')
    readonly_fields = ['customeruser']
