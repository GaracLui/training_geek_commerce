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
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
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
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/', 
        null=True, 
        blank=True, 
        verbose_name="Imagen Principal"
        )

    # LA MAGIA DE POSTGRESQL: JSONField
    # Aquí se guarda atributos únicos sin crear más tablas.
    # Ej para Manga: {"autor": "Akira Toriyama", "volumen": 4}
    # Ej para Juego: {"jugadores": "2-4", "edad": "+12"}
    specifications = models.JSONField(default=dict, blank=True, null=True, verbose_name="Especificaciones")

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
        ]
        verbose_name_plural = "Productos"


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

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['sku']),
        ]
        verbose_name_plural = "Variantes de Producto"

    def get_price(self):
        return self.product.base_price + self.price_adjustment

    def __str__(self):
        return f"{self.product.name} - {self.name}"


