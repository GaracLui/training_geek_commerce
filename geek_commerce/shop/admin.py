from django.contrib import admin
from django.db.models import JSONField
from django.utils.html import mark_safe # Para mostrar vista previa
from django_json_widget.widgets import JSONEditorWidget
from .models import Category, Brand, Product, ProductVariant, ProductImage

# Register your models here.
# --- CONFIGURACIÓN DE INLINES (Tablas dentro de otras tablas) ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # Cuántos espacios vacíos mostrar por defecto
    readonly_fields = ['image_preview'] # Opcional: para ver la foto cargada

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 50px; border-radius: 5px;" />')
        return "No image"
    image_preview.short_description = "Vista Previa"

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Muestra 1 fila vacía para agregar variantes rápido
    show_change_link = True # Permite ir a la edición completa de la variante

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

    inlines = [ProductVariantInline] # Aquí conectamos las variantes al producto

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'sku', 'brand','price', 'is_master')
    list_filter = ('product', 'is_master', 'brand', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('product', 'name')}

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('variant', 'image_preview', 'alt_text', 'is_main')
    list_filter = ('variant', 'is_main')
    search_fields = ('variant__name', 'is_main')
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 50px; border-radius: 5px;" />')
        return "No image"
    image_preview.short_description = "Vista Previa"
