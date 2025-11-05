# NoteSafe
Aplicación de notas personales segura (Django).

## Requisitos
- Python 3.x
- Django 4.2
- argon2-cffi

## Instalación
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## Puntos de seguridad implementados
- Contraseñas con Argon2
- CSRF activado
- Validación server-side en formularios
- ORM de Django (evita inyección SQL)
- Auditoría de registro/login/CRUD
