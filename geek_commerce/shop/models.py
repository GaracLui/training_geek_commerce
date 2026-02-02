from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
# CATEGORÍAS DE PRODUCTOS
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    # Permite subcategorías
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, verbose_name="Categoría Padre")

    class Meta:
        verbose_name_plural = "Categorías"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# PRODUCTOS (padre)
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Categoría")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name="Descripción")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Base")
    is_active = models.BooleanField(default=True, verbose_name="¿Activo?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    # IMAGEN PRICIPAL
    # Necesita Pillow instalado: pip install Pillow
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Imagen Principal")

    # LA MAGIA DE POSTGRESQL: JSONField
    # Aquí se guarda atributos únicos sin crear más tablas.
    # Ej para Manga: {"autor": "Akira Toriyama", "volumen": 4}
    # Ej para Juego: {"jugadores": "2-4", "edad": "+12"}
    specifications = models.JSONField(default=dict, blank=True, null=True, verbose_name="Especificaciones")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# VARIANTES (Inventario Real)
# Esto soluciona el problema de las remeras (Talle/Color)
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE, verbose_name="Producto")
    name = models.CharField(max_length=200, verbose_name="Nombre de la Variante")

    # Si esta variante cuesta más que el precio base, se suma aquí
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Ajuste de Precio")

    # CONTROL DE STOCK
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU (Código único de inventario)")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad en Stock")

    def get_price(self):
        return self.product.base_price + self.price_adjustment

    def __str__(self):
        return f"{self.product.name} - {self.name}"


# PEDIDO (la cabecera)
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('shipped', 'Enviado'),
        ('completed', 'Completado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE, verbose_name="Usuario")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    is_paid = models.BooleanField(default=False, verbose_name="¿Pagado?")   

    # Datos de envío
    shipping_address = models.TextField(verbose_name="Dirección de Envío")

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.user.username}"



# ÍTEM DEL PEDIDO (detalle)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Pedido")
    variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.CASCADE, verbose_name="Variante de Producto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    # CAMPO PARA PRPDUCTOS PERSONALIZADOS
    # Aquí el usuario escribe "Quiero que diga 'Feliz Cumple'" o sube un link a un archivo vectorial .webp, png, etc.
    customization_details = models.TextField(blank=True, null=True, verbose_name="Detalles de Personalización")

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.variant.name}"