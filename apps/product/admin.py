from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInLine(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine]


admin.site.register(Product, ProductAdmin)