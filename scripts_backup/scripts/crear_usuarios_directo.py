import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from gestion_calificaciones.models import Usuario

def crear_usuario(username, password, email, first_name, last_name, tipo_usuario):
    if not Usuario.objects.filter(username=username).exists():
        usuario = Usuario(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        usuario.set_password(password)
        usuario.save()
        print(f'Usuario {username} creado')
        return usuario
    else:
        print(f'Usuario {username} ya existe')
        return None

# Crear usuarios
print('Creando usuarios administradores...')
crear_usuario('director', 'director123', 'director@escuela63.edu.mx', 'Vitalicio', 'García López', 'admin')
crear_usuario('secretaria', 'secretaria123', 'secretaria@escuela63.edu.mx', 'María', 'González', 'admin')
crear_usuario('angel', 'angel123', 'angel@escuela63.edu.mx', 'Angel', 'Velasco', 'admin')
