#!/usr/bin/env bash
# Salir si hay un error
set -o errexit

# --- Limpiar estáticos previos para evitar errores de WhiteNoise ---
rm -rf staticfiles

# 1. Instalar librerías
pip install -r requirements.txt

# 2. Archivos estáticos
# Añadimos --clear para asegurar que los estilos del admin se regeneren correctamente
python manage.py collectstatic --no-input --clear

# 3. Migraciones de base de datos
python manage.py migrate

# 4. ACTUALIZAR O CREAR SUPERUSUARIO (Sin borrar)
echo "Configurando superusuario keyner..."
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
user, created = User.objects.get_or_create(username='keyner', defaults={'email': 'keyner@gmail.com'}); \
user.set_password('123'); \
user.is_superuser = True; \
user.is_staff = True; \
user.save(); \
print('Superusuario keyner actualizado con éxito')" \
| python manage.py shell