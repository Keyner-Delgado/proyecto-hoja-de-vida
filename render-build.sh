#!/usr/bin/env bash
# Salir inmediatamente si ocurre un error
set -o errexit

# 1. Instalar todas las librerías de tu requirements.txt
pip install -r requirements.txt

# 2. Recolectar archivos estáticos (CSS, JS) usando Whitenoise
# Esto los guardará en la carpeta 'staticfiles' que configuramos
python manage.py collectstatic --no-input

# 3. Aplicar migraciones a la base de datos PostgreSQL de Render
python manage.py migrate

# CREAR SUPERUSUARIO AUTOMÁTICO
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "Creando superusuario..."
  python manage.py createsuperuser \
    --no-input \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL || true
fi