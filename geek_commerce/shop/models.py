import uuid
import os

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    '''
    Modelo para categorías de productos. Permite subcategorías mediante la relación self-referencial.
        - name: Nombre de la categoría.
        - slug: Slug único para URLs amigables.
        - parent: Relación opcional a sí misma para permitir subcategorías.
        - Meta:
            - ordering: Ordena por nombre al recuperar categorías.
            - indexes: Índice en el campo 'name' para búsquedas rápidas.
            - verbose_name_plural: Nombre plural para la administración de Django.
        - save: Sobrescribe el método save para generar automáticamente el slug a partir del nombre si no se proporciona.
        - __str__: Devuelve el nombre de la categoría como representación de cadena.

    '''
    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL, verbose_name="Categoría Padre")

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


class Brand(models.Model):
    '''
    Modelo para marcas de productos.
        - name: Nombre de la marca.
        - slug: Slug único para URLs amigables.
        - Meta:
            - ordering: Ordena por nombre al recuperar marcas.
            - indexes: Índice en el campo 'name' para búsquedas rápidas.
            - verbose_name_plural: Nombre plural para la administración de Django.
        - save: Sobrescribe el método save para generar automáticamente el slug a partir del nombre si no se proporciona.
        - __str__: Devuelve el nombre de la marca como representación de cadena.
    '''
    name = models.CharField(max_length=200, verbose_name="Nombre de la Marca")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name_plural = "Marcas"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# PRODUCTOS (padre)
class Product(models.Model):
    '''
    Modelo para productos. Cada producto puede tener múltiples variantes (ProductVariant) que representan diferentes versiones del mismo producto (ej: diferentes colores, tallas, etc.).
        - category: Relación con el modelo Category para clasificar el producto.
        - name: Nombre del producto.
        - slug: Slug único para URLs amigables.
        - description: Descripción detallada del producto.
        - base_specs: Campo JSON para almacenar especificaciones base del producto (ej: material, dimensiones).
        - is_active: Indica si el producto está activo y disponible para la venta.
        - Meta:
            - ordering: Ordena por nombre al recuperar productos.
            - indexes: Índices en los campos 'name', 'category' y 'created_at' para búsquedas rápidas.
            - verbose_name_plural: Nombre plural para la administración de Django.
        - save: Sobrescribe el método save para generar automáticamente el slug a partir del nombre si no se proporciona.
        - __str__: Devuelve el nombre del producto como representación de cadena.
    '''
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT, verbose_name="Categoría")
    name = models.CharField(max_length=300, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name="Descripción")
    base_specs = models.JSONField(default=dict, blank=True, null=True, verbose_name="Especificaciones Base")
    is_active = models.BooleanField(default=True, verbose_name="¿Activo?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

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


class ProductVariant(models.Model):
    '''
    Modelo para variantes de productos. Cada variante representa una versión específica de un producto (ej: un producto "Camiseta" puede tener variantes "Camiseta Roja - Talla M", "Camiseta Azul - Talla L", etc.).
        - product: Relación con el modelo Product (producto padre).
        - name: Nombre de la variante (ej: "Roja - Talla M").
        - slug: Slug único para URLs amigables.
        - sku: Código único de inventario generado automáticamente.
        - brand: Relación opcional con el modelo Brand para asociar una marca a la variante.
        - description: Descripción detallada de la variante.
        - attributes: Campo JSON para almacenar atributos específicos de la variante (ej: color, talla).
        - weight_g: Peso de la variante en gramos.
        - price: Precio base de la variante.
        - is_master: Indica si esta variante es la principal del producto (la que se muestra por defecto).
        - Meta:
            - ordering: Ordena por nombre al recuperar variantes.
            - indexes: Índices en los campos 'name', 'slug', 'sku', 'product', 'brand' y 'created_at' para búsquedas rápidas.
            - verbose_name_plural: Nombre plural para la administración de Django.
        - save: Sobrescribe el método save para generar automáticamente el slug a partir del nombre si no se proporciona.
        - __str__: Devuelve una representación de cadena que indica el nombre del producto y el nombre de la variante.
    '''
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE, verbose_name="Producto")
    name = models.CharField(max_length=300, verbose_name="Nombre de la Variante")
    slug = models.SlugField(unique=True, blank=True)
    sku = models.UUIDField(unique=True, editable=False, default=uuid.uuid7, verbose_name="SKU (Código único de inventario)")
    brand = models.ForeignKey(Brand, related_name='products', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Marca")
    description = models.TextField(verbose_name="Descripción de la Variante", blank=True)
    attributes = models.JSONField(default=dict, blank=True, null=True, verbose_name="Atributos Específicos (ej: color, talla)")
    weight_g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Peso en gramos")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Base")
    is_master = models.BooleanField(default=False, verbose_name="¿Es la Variante del producto Principal?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['sku']),
            models.Index(fields=['product']),
            models.Index(fields=['brand']),
            models.Index(fields=['created_at']),
        ]
        verbose_name_plural = "Variantes de Producto"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.product.slug} {self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.name}"



# FUNCIÓN DE UTILIDAD 
def get_upload_path(instance, filename):
    '''
    Función para generar una ruta de carga personalizada para las imágenes de las variantes de productos.
    La ruta se construye de la siguiente manera:
        products/variants/<slug-de-la-variante>/<nombre-generado-único>.<extensión>
    Esto ayuda a mantener las imágenes organizadas por variante y evita conflictos de nombres.
    '''
    # Obtenemos la extensión del archivo original (ej: .webp, .png)
    ext = filename.split('.')[-1]
    
    # Construimos un nombre limpio usando el Slug de la variante
    # Esto ayuda al SEO y mantiene el orden.
    base_name = instance.variant.slug

    # Generamos un código único corto 
    unique_id = uuid.uuid7().hex[:10]
    
    # Construimos el nombre final
    new_filename = f"{base_name}_{unique_id}.{ext}"
    # Retornamos la ruta completa:
    # Ej: products/variants/remera-roja-l/REM-RED-L.webp
    return os.path.join('products', instance.variant.product.slug, 'variants', instance.variant.slug, new_filename)


class ProductImage(models.Model):
    '''
    '''
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.CASCADE, 
        related_name='images', # Importante para acceder desde la variante: variant.images.all()
        verbose_name="Variante"
    )
    image = models.ImageField(
        upload_to=get_upload_path, # Carpeta donde se guardarán
        verbose_name="Imagen"
    )
    alt_text = models.CharField(max_length=300, blank=True, verbose_name="Texto Alternativo (SEO)")
    is_main = models.BooleanField(default=False, verbose_name="¿Es la principal?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"
    
    def __str__(self):
        return f"Imagen {self.id} de {self.variant.sku}"
