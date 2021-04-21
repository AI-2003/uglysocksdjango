from django.contrib import admin

# Register your models here.
from .models import Product, Order, ProductImage, Review, Address, StripeReceipt, CustomImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ReviewInline(admin.TabularInline):
    model = Review

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ReviewInline
    ]


class OrderAddress(admin.TabularInline):
    model = Address
class OrderReceipt(admin.TabularInline):
    model = StripeReceipt
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderAddress,
        OrderReceipt
    ]
    fields = ("id", "created", "received", "total", "status", "products")
    readonly_fields=("id", "created")
    list_filter=("status",)

class CustomImageAdmin(admin.ModelAdmin):
    fields = ("uuid", "front", "back", "status")
    readonly_fields=("uuid",)
    list_filter=("status",)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CustomImage, CustomImageAdmin)