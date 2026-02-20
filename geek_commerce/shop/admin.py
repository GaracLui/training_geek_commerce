from django.contrib import admin
from django.db.models import JSONField
from django.utils.html import mark_safe # Para mostrar vista previa
from django_json_widget.widgets import JSONEditorWidget
from .models import Category, Brand, Product, ProductVariant, ProductImage

# Register your models here.
# --- CONFIGURACIÓN DE INLINES (Tablas dentro de otras tablas) ---
class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1 # Cuántos espacios vacíos mostrar por defecto
    show_change_link = True # Permite ir a la edición completa de la imagen
    readonly_fields = ['image_preview'] # Opcional: para ver la foto cargada

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 50px; border-radius: 5px;" />')
        return "No image"
    image_preview.short_description = "Vista Previa"

class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 1  # Muestra 1 fila vacía para agregar variantes rápido
    show_change_link = True # Permite ir a la edición completa de la variante
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

# --- CONFIGURACIÓN DE LOS PANELES PRINCIPALES ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent',)
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información General', {
            'fields': (
                'name', 'description', 'category', 'is_active'
            ),
        }),
        ('Detalles Generales de todas sus variantes', {
            'classes': ('collapse',),
            'fields': (
                'base_specs',
            ),
        }),
        ('Fecha de Creación y Actualización', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    inlines = [
        ProductVariantInline,
    ]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'slug', 'sku', 'brand','price', 'is_master')
    list_filter = ('product', 'is_master', 'brand', 'created_at')
    search_fields = ('name', 'description', 'product__name', 'brand__name')
    readonly_fields = ['sku','created_at', 'updated_at']


    fieldsets = (
        ('Información general', {
            'fields': (
                'name', 'description', 'product', 'brand',
            ),
        }),
        ('Detalles del producto',{
            'classes': ('collapse',),
            'fields': (
                'attributes', 'price','weight_g', 'is_master',
            ),
        }),
        ('Fecha de Creación y Actualización', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('variant', 'image_preview', 'alt_text', 'is_main')
    list_filter = ('variant', 'is_main', 'created_at')
    search_fields = ('variant__name', 'is_main', 'alt_text')
    readonly_fields = ['image_preview', 'created_at', 'updated_at']

    fieldsets = (
        ('Imagen y Detalles', {
            'fields': ('image', 'alt_text'),
            'classes': ('collapse',),
        }),
        ('Producto información', {
            'fields': (
                'variant', 'is_main'
            ),
        }),
    )
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 50px; border-radius: 5px;" />')
        return "No image"
    image_preview.short_description = "Vista Previa"


admin.site.site_header = "Geek Commerce Admin"
admin.site.site_title = "Geek Commerce Admin Portal"
admin.site.index_title = "Bienvenido al Panel de Administración de Geek Commerce"

