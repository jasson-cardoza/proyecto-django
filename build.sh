#!/usr/bin/env bash

# Detener el despliegue si ocurre algún error
set -o errexit

# Instalar las dependencias
pip install -r requirements.txt

# Preparar los archivos estáticos
python manage.py collectstatic --no-input

# Aplicar las migraciones de Django
python manage.py migrate --noinput

# Diagnóstico temporal (no imprime el valor)
if [ -z "$DATABASE_URL" ]; then
  echo ">>> DATABASE_URL NO está definida en el build"
else
  echo ">>> DATABASE_URL sí está definida"
fi

# Crear el superusuario con las variables DJANGO_SUPERUSER_* (si ya existe, no pasa nada)
python manage.py createsuperuser --noinput || true