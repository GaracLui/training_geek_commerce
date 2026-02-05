![Estado del Proyecto](https://img.shields.io/badge/Estado-En_Desarrollo-yellow)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-4.x-green)

## 📋 Descripción

Este proyecto es una plataforma de comercio electrónico (E-commerce) desarrollada con **Django**. El objetivo es simular una tienda en línea enfocada en productos de nicho y hobbies, tales como juegos de mesa, literatura fantástica, manga, indumentaria y artículos personalizados.

El proyecto forma parte de mi portafolio personal y busca demostrar la implementación de un flujo completo de compra, gestión de usuarios y administración de inventario.

## 🚀 Funcionalidades Principales

* **Catálogo de Productos:** Vista de listado y detalle para diversas categorías (Libros, Rol, Accesorios, etc.).
* **Sistema de Carrito:** Lógica de sesiones para agregar/quitar productos sin necesidad de loguearse inicialmente.
* **Gestión de Variantes:** Soporte para productos con talles y colores (ej. remeras) y productos simples (ej. juegos de mesa).
* **Personalización:** Campo para subir detalles en pedidos personalizados (ej. texto para una cartuchera).
* **Checkout:** Proceso de finalización de compra.
* **Panel de Administración:** Uso del Django Admin para gestionar stock, precios y pedidos.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django Framework.
* **Base de Datos:** PostgreSQL (Producción).
* **Frontend:** Django Templates, Tailwind CSS.
* **Control de Versiones:** Git & GitHub.

## 💻 Instalación y Puesta en Marcha

### Virtual Environment y Packages

* **crear virtual environment:** navega al directorio del proyecto en Git Bash. Después corre el siguiente comando:

   ```
   python -m venv venv
   ```

* **activar virtual environment:** corre el siguiente comando para activar el environment:
   ```
   source venv/Scripts/activate
   ```

* **instalar packages:**
   ```
   pip install -r requirements.txt
   ```
### .env

* crea un archivo `.env` conteniedo las siguientes variables (puedes alterar los valores).
  ```
  POSTGRES_DB=dev_database
  POSTGRES_USER=catanist
  POSTGRES_PASSWORD=catan_champion
  DB_HOST=db
  DB_PORT=5432

  SECRET_KEY='django-insecure-@5^@yns$uk#=($wel3r4w-*d0+rj&j207*rzo=$tu9*uv(10m)'
  DEBUG=True
  ```

### Docker

* crea (o reconstruye) las imágenes para todos los servicios definidos en su archivo `docker-compose.yaml` y luego crea, inicia y adjunta los contenedores para esos servicios.
  ```
  docker-compose up --build
  ```
* realiza una migración basada en los modelos de Django (estando activo Docker).
  ```
  docker exec geek_commerce_web python manage.py makemigrations
  ```
* aplica las migraciones.
  ```
  docker exec geek_commerce_web python manage.py migrate
  ```

* comprueba de que se a creado correctamente la base de datos.
  ```
  docker exec -ti postgres_db psql -U catanist -d dev_database
  ```
  y ejecuta el comando para mostrar las entidades.
  ```
  \dt
  ```
## 📷 Capturas de Pantalla



## ⚠️ Disclaimer

Este es un proyecto con fines educativos y de demostración. Las imágenes de productos (libros, juegos, personajes) utilizadas en la base de datos de prueba pertenecen a sus respectivos autores y marcas registradas. No existe intención comercial real ni lucro con la propiedad intelectual de terceros.

## ✒️ Autor

   Garacciolo Luis Alfredo

   www.linkedin.com/in/garacciolo-luis-alfredo

Hecho con ❤️ y Python.
