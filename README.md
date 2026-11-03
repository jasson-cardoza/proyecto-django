# Proyecto ReciclaCerca

## Descripción

ReciclaCerca es un proyecto desarrollado con Python y Django. Su objetivo es servir como base para el desarrollo de una aplicación relacionada con el reciclaje.

El proyecto utiliza SQL Server como sistema de gestión de base de datos y busca mantener una estructura organizada, aplicando conceptos de programación orientada a objetos y separación de módulos.

## Repositorio

GitHub: [https://github.com/jasson-cardoza/proyecto-django](https://github.com/jasson-cardoza/proyecto-django)

## Tecnologías utilizadas

- Python
- Django
- SQL Server
- mssql-django
- pyodbc
- Git y GitHub

## Requisitos previos

Para ejecutar el proyecto, es necesario tener instalado:

- Python
- SQL Server
- Microsoft ODBC Driver para SQL Server
- Git

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/jasson-cardoza/proyecto-django.git
cd proyecto-django
```


### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En Windows CMD:

```bash
venv\Scripts\activate
```

En PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Actualizar pip

```bash
python -m pip install --upgrade pip
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 6. Configurar la base de datos

Crear la base de datos de ReciclaCerca en SQL Server (el script está en `database/ProyectoReciclaCerca.sql`) y configurar los datos de conexión en `settings.py`.

La configuración debe incluir el nombre de la base de datos, el servidor y el método de autenticación correspondiente.

Las credenciales no deben publicarse en GitHub.

### 7. Variables de entorno (opcional en desarrollo)

La clave secreta de Django no está en el código; se lee de la variable `DJANGO_SECRET_KEY`. Para desarrollo local no hace falta configurarla (se usa una clave de prueba). En producción es obligatoria y `DJANGO_DEBUG` debe ser `False`.

Generar una clave:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

Definirla en PowerShell (solo para esa terminal):

```powershell
$env:DJANGO_SECRET_KEY = "pega-aqui-la-clave"
```

### 8. Ejecutar las migraciones

Los comandos de `manage.py` se ejecutan en la raíz del repositorio (donde está `manage.py`):

```bash
python manage.py migrate
```

### 9. Comprobar la configuración de Django

```bash
python manage.py check
```

### 10. Iniciar el servidor

```bash
python manage.py runserver
```

Abrir en el navegador:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 11. (Opcional) Cargar datos de ejemplo

Carga materiales, puntos de reciclaje de Chalatenango (El Salvador), usuarios de prueba, registros y reportes:

```bash
python manage.py cargar_datos_ejemplo
```

Para borrar los datos de ejemplo y cargarlos de nuevo: `python manage.py cargar_datos_ejemplo --reiniciar`.
Los usuarios de prueba (`ana_martinez`, `carlos_hernandez`, `maria_rivas`, `ecochalate_sv`) usan la contraseña `Reciclar2026`.
El administrador se crea con `python manage.py createsuperuser`.

## Estructura del proyecto

El proyecto sigue la arquitectura estándar de Django: un **paquete de configuración** (`config/`) y varias **aplicaciones**, cada una con una única responsabilidad. Cada aplicación es dueña de sus modelos, vistas, plantillas y rutas (`urls.py`); el `urls.py` de `config/` solo las enlaza.

### Árbol de carpetas y archivos

```text
proyecto-django/                      # Raíz del repositorio (aquí está manage.py)
├── manage.py                         # Utilidad de línea de comandos de Django
├── README.md                         # Documentación principal
├── requirements.txt                  # Dependencias de Python
├── .gitignore                        # Archivos ignorados por Git
│
├── config/                           # Configuración del proyecto
│   ├── settings.py                   # Apps instaladas, base de datos, plantillas, estáticos...
│   ├── urls.py                       # Rutas raíz: enlaza las rutas de cada aplicación
│   ├── asgi.py                       # Punto de entrada ASGI
│   └── wsgi.py                       # Punto de entrada WSGI
│
├── database/
│   └── ProyectoReciclaCerca.sql      # Script SQL que crea la base de datos en SQL Server
│
├── static/                           # Archivos estáticos compartidos
│   └── css/
│       └── estilos.css               # Estilos propios (se cargan después de Bootstrap)
│
├── templates/                        # Plantillas compartidas por todas las apps
│   ├── base.html                     # Estructura común: navbar, mensajes y pie de página
│   └── includes/
│       ├── campos.html               # Pinta los campos de un formulario
│       └── paginacion.html           # Controles de paginación de las listas
│
├── inicio/                           # App: portada
│   ├── apps.py, urls.py, views.py, tests.py
│   └── templates/inicio/inicio.html
│
├── usuarios/                         # App: cuentas, inicio de sesión, perfiles y direcciones
│   ├── admin.py, apps.py, forms.py, models.py, tests.py, urls.py, views.py
│   ├── mixins.py                     # Permisos compartidos (solo staff, solo mis datos, perfil requerido)
│   ├── migrations/
│   └── templates/usuarios/           # login, perfil_*, direccion_*
│
├── reciclaje/                        # App: materiales, puntos de reciclaje y registros
│   ├── admin.py, apps.py, models.py, tests.py, urls.py, views.py
│   ├── utils.py                      # Funciones auxiliares (también las usa reportes)
│   ├── migrations/
│   ├── management/commands/
│   │   └── cargar_datos_ejemplo.py   # Comando para cargar datos de ejemplo
│   └── templates/reciclaje/          # material_*, punto_*, registro_*
│
└── reportes/                         # App: reportes ciudadanos y su seguimiento
    ├── admin.py, apps.py, models.py, tests.py, urls.py, views.py
    ├── migrations/
    └── templates/reportes/           # reporte_*, seguimiento_*
```

> El entorno virtual (`venv/` o `.venv/`) vive en la raíz solo en tu máquina y no se versiona.

### Dónde va cada plantilla

- Lo que usan **todas** las páginas (`base.html` y los fragmentos de `includes/`) está en `templates/` y se carga con `{% extends 'base.html' %}` o `{% include 'includes/campos.html' %}`.
- Lo que es de **una sola app** está en `<app>/templates/<app>/` (por ejemplo `reciclaje/templates/reciclaje/material_list.html`). Las vistas lo indican con `template_name`.

### Responsabilidad de cada aplicación

| Aplicación | Responsabilidad | Ruta base |
| --- | --- | --- |
| `inicio` | Portada del sitio. | `/` |
| `usuarios` | Registro, inicio y cierre de sesión, perfiles y direcciones. | `/usuarios/` |
| `reciclaje` | Materiales, puntos de reciclaje y registros de reciclaje (con sus puntos). | `/reciclaje/` |
| `reportes` | Reportes ciudadanos (punto lleno, contenedor dañado...) y sus comentarios de seguimiento. | `/reportes/` |

### Dependencias entre aplicaciones

Las dependencias van en un solo sentido, para evitar importaciones circulares:

| Aplicación | Puede depender de |
| --- | --- |
| `inicio` | Ninguna |
| `usuarios` | `django.contrib.auth` |
| `reciclaje` | `usuarios` |
| `reportes` | `reciclaje` y `usuarios` |

Por ejemplo, `reciclaje` puede importar de `usuarios`, pero `usuarios` nunca importa de `reciclaje` ni de `reportes`.

Lo que comparten varias apps vive en archivos propios, no en las vistas: los permisos en `usuarios/mixins.py` y las funciones auxiliares de reciclaje en `reciclaje/utils.py`.

### Archivos estándar de cada aplicación

| Archivo o carpeta | Para qué sirve |
| --- | --- |
| `models.py` | Clases (modelos) que representan los datos de la app y se guardan en la base de datos. |
| `views.py` | Vistas: reciben la petición HTTP y devuelven la respuesta. |
| `urls.py` | Rutas de la app. Define `app_name` como espacio de nombres (ej. `inicio:inicio`). |
| `admin.py` | Registro de los modelos en el panel de administración de Django. |
| `apps.py` | Configuración de la app: nombre, nombre visible y su responsabilidad. |
| `tests.py` | Pruebas automáticas. |
| `migrations/` | Historial de cambios de los modelos sobre la base de datos (se genera con `makemigrations`). |
| `templates/<app>/` | Plantillas HTML de la app. |

`inicio` no define modelos, por eso no tiene `models.py`, `admin.py` ni `migrations/`.

### Cómo agregar una nueva aplicación

Desde la raíz del repositorio (donde está `manage.py`):

1. Crearla: `python manage.py startapp nombre`.
2. Crear `nombre/urls.py` con `app_name = 'nombre'` y una lista `urlpatterns`.
3. Agregar `'nombre'` a `INSTALLED_APPS` en `config/settings.py`.
4. Enlazarla en `config/urls.py` con `path('nombre/', include('nombre.urls'))`.
5. Documentar su responsabilidad en su `apps.py` y en esta sección.

## Integrantes
* **Jose Leonel Acevedo Villacorta**
* **Henry Abdiel Andrade Gomez**
* **Mario Antonio Portillo Rivera**
* **Jasson Wilfredo Cardoza Chiquillo**
* **Edgar Alexander Avelar Rivera**



