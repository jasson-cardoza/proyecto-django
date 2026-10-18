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

La estructura inicial incluye el proyecto principal de Django, una aplicación para organizar la funcionalidad y los archivos necesarios para su configuración.

```text
Proyecto_POO/
├── .vscode/
│   └── settings.json          # Configuración del entorno en VS Code
├── src/
│   ├── models/                # Clases, objetos y lógica del dominio (POO)
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   └── usuario.py
│   ├── services/              # Integraciones externas y servicios
│   │   ├── __init__.py
│   │   └── servicio.py
│   ├── utils/                 # Funciones auxiliares y herramientas
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── __init__.py
│   └── main.py                # Punto de entrada de la aplicación
├── tests/                     # Pruebas unitarias
│   ├── __init__.py
│   └── test_main.py
├── .gitignore                 # Archivos y carpetas ignorados por Git (ej. env/)
├── README.md                  # Documentación principal
└── requirements.txt           # Dependencias del proyecto
```
## Integrantes
* **Jose Leonel Acevedo Villacorta**
* **Henry Abdiel Andrade Gomez**
* **Mario Antonio Portillo Rivera**
* **Jasson Wilfredo Cardoza Chiquillo**
* **Edgar Alexander Avelar Rivera**



