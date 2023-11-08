from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "unit_price", "quantity_on_hand"]
    list_filter = ["quantity_on_hand", "name", "unit_price"]
    search_fields = ["name", "unit_price", "quantity_on_hand"]
    search_help_text = "Search for product by name, unit price or quantity on hand."
    ordering = ["name", "unit_price", "quantity_on_hand"]
    fieldsets = (
        ("Main Information", {
            "fields": ("name", "description")
        }),
        ("Inventory Information", {
            "fields": ("unit_price", "quantity_on_hand")
        }),
        ('Others', {
            'fields': ('image',)
        })
    )

    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone_number", "email", "address"]
    ordering = ["first_name"]

    search_fields = ["first_name", "last_name", "email"]
    search_help_text = "Search for customers by first name, last name or email"
    fieldsets = (
        ("Basic Information", {
            "fields": ("first_name", "last_name")
        }),
        ("Contact Information", {
            "fields": ("email", "phone_number", "address")
        })
    )
    pass


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["customer", "product", "quantity_sold", "sale_date"]
    list_filter = ["quantity_sold", "sale_date"]
    date_hierarchy = 'sale_date'
    ordering = ["-sale_date", "quantity_sold"]
    search_fields = ["quantity_sold"]
    search_help_text = "Search Sale record by quantity sold"
    readonly_fields = ('sale_date',)
    fieldsets = (
        ("Sales Information", {
            "fields": ("customer", "product")
        }),
        ("Inventory Information", {
            "fields": ["quantity_sold", "sale_date"]
        })
    )
    pass


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ["product", "revenue"]
    list_filter = ["sales_count"]
    search_fields = ["sales_count"]
    search_help_text = "Search Analytics by sales count"
    ordering = ["revenue"]
    pass
