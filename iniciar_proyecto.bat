@echo off
echo Iniciando Sistema de Calificaciones...
call venv\Scripts\activate
python manage.py migrate
python manage.py inicializar
python manage.py runserver