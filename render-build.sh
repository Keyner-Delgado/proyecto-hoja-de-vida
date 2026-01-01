#!/usr/bin/env bash
# Salir si hay un error
set -o errexit

# 1. Instalar librerías
pip install -r requirements.txt

# 2. Archivos estáticos
python manage.py collectstatic --no-input

# 3. Migraciones de base de datos
python manage.py migrate

# 4. CREAR SUPERUSUARIO FORZADO (Método Shell)
echo "Forzando creación de superusuario..."
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='keyner').delete(); \
User.objects.create_superuser('keyner', 'keyner@gmail.com', '123')" \
| python manage.py shell