#!/usr/bin/env bash

# Detener el despliegue si ocurre algún error
set -o errexit

# Instalar las dependencias
pip install -r requirements.txt

# Preparar los archivos estáticos
python manage.py collectstatic --no-input

# Aplicar las migraciones de Django
python manage.py migrate --noinput
