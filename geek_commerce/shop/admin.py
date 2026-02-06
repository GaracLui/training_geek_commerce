from django.contrib import admin
from .models import Category, Product, ProductVariant

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    list_editable = ('is_active','base_price')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'sku', 'price_adjustment', 'stock_quantity')
    list_filter = ('product',)
    search_fields = ('name', 'sku')