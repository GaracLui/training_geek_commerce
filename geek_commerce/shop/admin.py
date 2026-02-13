from django.contrib import admin
from .models import Category, Product, ProductVariant

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'is_active', 'created_at')
    list_filter = ('category', 'brand', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product_Variant)
class Product_VariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'sku', 'price', 'is_master')
    list_filter = ('product', 'is_master')
    search_fields = ('name', 'sku')
    prepopulated_fields = {'sku': ('product', 'name')}