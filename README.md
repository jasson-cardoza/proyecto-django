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

Crear la base de datos de ReciclaCerca en SQL Server y configurar los datos de conexión en `settings.py`.

La configuración debe incluir el nombre de la base de datos, el servidor y el método de autenticación correspondiente.

Las credenciales no deben publicarse en GitHub.

### 7. Ejecutar las migraciones

Los comandos de `manage.py` (este paso y los siguientes) se ejecutan dentro de la carpeta `Proyecto_ReciclaCerca/`:

```bash
cd Proyecto_ReciclaCerca
```

```bash
python manage.py migrate
```

### 8. Comprobar la configuración de Django

```bash
python manage.py check
```

### 9. Iniciar el servidor

```bash
python manage.py runserver
```

Abrir en el navegador:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Estructura del proyecto

El proyecto sigue la arquitectura estándar de Django: un **proyecto de configuración** (`Proyecto_ReciclaCerca`) y varias **aplicaciones**, cada una con una única responsabilidad. Cada aplicación es dueña de sus modelos, vistas, plantillas y rutas (`urls.py`); el `urls.py` del proyecto solo las enlaza.

### Árbol de carpetas y archivos

```text
Proyecto_POO/                         # Raíz del repositorio (se llama proyecto-django/ al clonarlo)
├── .gitignore                        # Archivos ignorados por Git (__pycache__/, *.pyc)
├── README.md                         # Documentación principal
├── requirements.txt                  # Dependencias de Python
└── Proyecto_ReciclaCerca/            # Carpeta del proyecto Django (aquí está manage.py)
    ├── manage.py                     # Utilidad de línea de comandos de Django
    │
    ├── Proyecto_ReciclaCerca/        # Paquete de configuración del proyecto
    │   ├── __init__.py
    │   ├── settings.py               # Configuración: apps instaladas, base de datos, idioma...
    │   ├── urls.py                   # Rutas raíz: enlaza las rutas de cada aplicación
    │   ├── asgi.py                   # Punto de entrada ASGI
    │   ├── wsgi.py                   # Punto de entrada WSGI
    │   └── ProyectoReciclaCerca.sql  # Script SQL que crea la base de datos en SQL Server
    │
    ├── inicio/                       # App: páginas públicas (portada e información general)
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── migrations/
    │   │   └── __init__.py
    │   └── templates/
    │       └── inicio/
    │           └── Plantilla.html    # Portada del sitio
    │
    ├── usuarios/                     # App: cuentas, autenticación, perfiles y roles
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │   └── migrations/
    │       └── __init__.py
    │
    ├── reciclaje/                    # App: dominio principal (materiales, puntos y registros de reciclaje)
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │   └── migrations/
    │       └── __init__.py
    │
    └── reportes/                     # App: estadísticas y reportes (solo lectura)
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── tests.py
        ├── urls.py
        ├── views.py
        └── migrations/
            └── __init__.py
```

> El entorno virtual (`venv/` o `env/`) vive en la raíz solo en tu máquina y no se versiona.

### Responsabilidad de cada aplicación

| Aplicación | Responsabilidad | Ruta base |
| --- | --- | --- |
| `inicio` | Páginas públicas: portada e información general sobre reciclaje. | `/` |
| `usuarios` | Cuentas de usuario: registro, inicio y cierre de sesión, perfiles y roles. | `/usuarios/` |
| `reciclaje` | Dominio principal: materiales, puntos de reciclaje y registros de reciclaje. | `/reciclaje/` |
| `reportes` | Estadísticas y reportes sobre lo reciclado. Solo lee datos; no define los suyos. | `/reportes/` |

### Dependencias entre aplicaciones

Las dependencias van en un solo sentido, para evitar importaciones circulares:

| Aplicación | Puede depender de |
| --- | --- |
| `inicio` | Ninguna |
| `usuarios` | `django.contrib.auth` |
| `reciclaje` | `usuarios` |
| `reportes` | `reciclaje` y `usuarios` (solo para leer datos) |

Por ejemplo, `reciclaje` puede importar de `usuarios`, pero `usuarios` nunca importa de `reciclaje` ni de `reportes`.

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
| `templates/<app>/` | Plantillas HTML de la app. Se crea cuando la app las necesita. |

### Estado actual

- `usuarios`, `reciclaje` y `reportes` están creadas y registradas en `INSTALLED_APPS`, pero todavía no tienen modelos, vistas ni plantillas. Mientras tanto, sus URLs (`/usuarios/`, `/reciclaje/`, `/reportes/`) responden 404.
- Los usuarios usan por ahora el modelo `User` que incluye Django. Si el equipo decide crear un modelo de usuario propio (`AUTH_USER_MODEL`), debe hacerse **antes de ejecutar `migrate` por primera vez**: cambiarlo después es muy complicado y normalmente obliga a recrear la base de datos.

### Cómo agregar una nueva aplicación

Desde `Proyecto_ReciclaCerca/` (la carpeta donde está `manage.py`):

1. Crearla: `python manage.py startapp nombre`.
2. Crear `nombre/urls.py` con `app_name = 'nombre'` y una lista `urlpatterns`.
3. Agregar `'nombre'` a `INSTALLED_APPS` en `Proyecto_ReciclaCerca/settings.py`.
4. Enlazarla en `Proyecto_ReciclaCerca/urls.py` con `path('nombre/', include('nombre.urls'))`.
5. Documentar su responsabilidad en su `apps.py` y en esta sección.

## Integrantes
* **Jose Leonel Acevedo Villacorta**
* **Henry Abdiel Andrade Gomez**
* **Mario Antonio Portillo Rivera**
* **Jasson Wilfredo Cardoza Chiquillo**
* **Edgar Alexander Avelar Rivera**



