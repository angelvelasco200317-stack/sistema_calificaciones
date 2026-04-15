import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from gestion_calificaciones.models import Usuario

def crear_usuarios_admin():
    usuarios_admin = [
        {
            'username': 'director',
            'password': 'director123',
            'email': 'director@escuela63.edu.mx',
            'first_name': 'Vitalicio',
            'last_name': 'García López',
            'tipo_usuario': 'admin'
        },
        {
            'username': 'secretaria',
            'password': 'secretaria123', 
            'email': 'secretaria@escuela63.edu.mx',
            'first_name': 'María',
            'last_name': 'González',
            'tipo_usuario': 'admin'
        },
        {
            'username': 'angel',
            'password': 'angel123',
            'email': 'angel@escuela63.edu.mx',
            'first_name': 'Angel',
            'last_name': 'Velasco',
            'tipo_usuario': 'admin'
        }
    ]
    
    for usuario_data in usuarios_admin:
        if not Usuario.objects.filter(username=usuario_data['username']).exists():
            usuario = Usuario.objects.create_user(
                username=usuario_data['username'],
                password=usuario_data['password'],
                email=usuario_data['email'],
                first_name=usuario_data['first_name'],
                last_name=usuario_data['last_name'],
                tipo_usuario=usuario_data['tipo_usuario']
            )
            print(f"Usuario admin creado: {usuario.username}")
        else:
            print(f"Usuario {usuario_data['username']} ya existe")

if __name__ == '__main__':
    crear_usuarios_admin()