# Kiosco Lista de Mercadería

**Trabajo Práctico Integrador — Programación Web**

**Estudiantes:** Máximo Padilla y Alexis Romero.

## Descripción

Kiosco Lista de Mercadería es un sistema web desarrollado con Django para facilitar el control y la administración de los productos de un kiosco escolar.

Permite registrar productos, consultar las cantidades disponibles, controlar el stock, registrar ingresos y movimientos de mercadería y llevar un control de los productos retirados.

## Tecnologías utilizadas

- Python 3.12
- Django 6.1.2
- HTML
- CSS
- JavaScript
- SQLite (si se conserva la configuración predeterminada del proyecto).

## Aplicaciones del sistema

- **Productos:** registro, consulta, búsqueda, edición y administración de productos.
- **Stocks:** control de cantidades disponibles y stock mínimo.
- **Mercadería retirada:** registro de productos retirados y sus motivos.

## Instalación y ejecución

### 1. Requisitos previos

Tener instalado Python y disponer de una terminal.

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

### 6. Crear un usuario administrador

```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

El sistema estará disponible en:

http://127.0.0.1:8000/

## Acceso al sistema

- Productos: `/productos/`
- Stock: `/stocks/`
- Mercadería retirada: `/mercaderia-retirada/`
- Inicio de sesión: `/cuentas/login/`
- Administración: `/admin/`

## Usuarios y permisos

El sistema contempla dos roles principales:

**Estudiantes:**
- Consultar productos.
- Consultar información y cantidades habilitadas.
- No pueden modificar el inventario ni eliminar registros sin autorización.

**Adultos responsables:**
- Registrar y modificar productos.
- Administrar el stock.
- Registrar ingresos y ventas.
- Registrar retiros y descartes.
- Consultar el historial de movimientos.

La autenticación y autorización se administran mediante el sistema de usuarios y grupos de Django.

## Archivos estáticos

Los archivos estáticos se organizan en la carpeta `static/`:

- `static/css/`: hojas de estilo.
- `static/js/`: archivos JavaScript.
- `static/img/`: imágenes del sistema.

## Autores

Máximo Padilla y Alexis Romero.

**Proyecto:** Kiosco Lista de Mercadería.