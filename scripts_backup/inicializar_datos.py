import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from gestion_calificaciones.models import Usuario, Materia

def crear_usuarios_iniciales():
    """Crear usuarios iniciales si no existen"""
    usuarios = [
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
        },
        {
            'username': 'profesor1',
            'password': 'profesor123',
            'email': 'profesor1@escuela63.edu.mx',
            'first_name': 'Carlos',
            'last_name': 'Martínez',
            'tipo_usuario': 'docente'
        }
    ]
    
    for usuario_data in usuarios:
        if not Usuario.objects.filter(username=usuario_data['username']).exists():
            usuario = Usuario.objects.create_user(**usuario_data)
            print(f"✅ Usuario creado: {usuario.username}")
        else:
            print(f"⚠️ Usuario {usuario_data['username']} ya existe")

def crear_materias_iniciales():
    """Crear materias iniciales si no existen"""
    materias = [
        {'nombre': 'Matemáticas', 'codigo': 'MAT001'},
        {'nombre': 'Español', 'codigo': 'ESP001'},
        {'nombre': 'Ciencias Naturales', 'codigo': 'CIE001'},
        {'nombre': 'Historia', 'codigo': 'HIS001'},
        {'nombre': 'Geografía', 'codigo': 'GEO001'},
        {'nombre': 'Formación Cívica y Ética', 'codigo': 'FCE001'},
        {'nombre': 'Inglés', 'codigo': 'ING001'},
    ]
    
    for materia_data in materias:
        if not Materia.objects.filter(codigo=materia_data['codigo']).exists():
            materia = Materia.objects.create(**materia_data)
            print(f"✅ Materia creada: {materia.nombre}")
        else:
            print(f"⚠️ Materia {materia_data['codigo']} ya existe")

if __name__ == '__main__':
    print("🚀 Inicializando datos del sistema...")
    crear_usuarios_iniciales()
    crear_materias_iniciales()
    print("🎉 Inicialización completada!")