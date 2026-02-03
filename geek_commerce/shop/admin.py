from django.contrib import admin
from django.utils.html import mark_safe # Para mostrar imágenes
from .models import Category, Product, ProductVariant, Order, OrderItem

# --- CONFIGURACIÓN DE CATEGORÍAS ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    search_fields = ('name',)
    # Genera el slug automáticamente mientras escribes el nombre
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)

# --- CONFIGURACIÓN DE PRODUCTOS ---

# Esto permite editar las variantes DENTRO de la pantalla del producto
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Muestra una línea vacía para agregar nueva variante
    show_change_link = True # Permite ir a editar la variante en detalle

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_with_image', 'category', 'base_price', 'is_active', 'variant_count')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline]
    
    # Campo para ver bien el JSON
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'image', 'base_price', 'is_active')
        }),
        ('Detalles Técnicos', {
            'classes': ('collapse',), # Esto hace que se pueda ocultar/mostrar
            'fields': ('specifications',)
        }),
    )

    # Función personalizada para mostrar miniatura de imagen
    def name_with_image(self, obj):
        if obj.image:
            # Usamos mark_safe para que Django renderice el HTML
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit:cover; border-radius:5px;" /> {obj.name}')
        return obj.name
    name_with_image.short_description = "Producto"

    # Función para contar cuántas variantes tiene
    def variant_count(self, obj):
        return obj.variants.count()
    variant_count.short_description = "Nº Variantes"


# --- CONFIGURACIÓN DE VARIANTES (Opcional, si quieres verlas sueltas) ---
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'sku', 'stock_quantity', 'get_final_price')
    search_fields = ('sku', 'product__name', 'name')
    list_filter = ('product__category',)
    list_editable = ('stock_quantity',) # ¡Súper útil! Edita stock sin entrar al detalle

    def get_final_price(self, obj):
        return f"${obj.get_price()}"
    get_final_price.short_description = "Precio Final"


# --- CONFIGURACIÓN DE PEDIDOS ---

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # No queremos agregar ítems vacíos manualmente por defecto
    readonly_fields = ('get_cost_display',) # Para ver el subtotal ahí mismo
    
    def get_cost_display(self, obj):
        return f"${obj.get_cost()}"
    get_cost_display.short_description = "Subtotal"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'is_paid', 'created_at', 'get_total_order')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'shipping_address', 'id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    # Acciones masivas (ej: Marcar varios como Enviados)
    actions = ['mark_as_shipped', 'mark_as_paid']

    def get_total_order(self, obj):
        return f"${obj.get_total_cost()}"
    get_total_order.short_description = "Total"

    @admin.action(description="Marcar seleccionados como Enviados")
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')

    @admin.action(description="Marcar seleccionados como Pagados")
    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True, status='paid')