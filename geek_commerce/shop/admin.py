from django.contrib import admin
from .models import Category, Brand, Product, Product_Variant

# Register your models here.

# --- CONFIGURACIÓN DE LOS PANELES PRINCIPALES ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    inlines = [Product_VariantInline] # Aquí conectamos las variantes al producto

@admin.register(Product_Variant)
class Product_VariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'sku', 'brand','price', 'is_master')
    list_filter = ('product', 'is_master')
    search_fields = ('name', 'sku')
    prepopulated_fields = {'sku': ('product', 'name')}


# --- CONFIGURACIÓN DE INLINES (Tablas dentro de otras tablas) ---

class Product_VariantInline(admin.TabularInline):
    model = Product_Variant
    extra = 1  # Muestra 1 fila vacía para agregar variantes rápido
    show_change_link = True # Permite ir a la edición completa de la variante