from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from .models import Usuario, Materia

@receiver(post_migrate)
def inicializar_datos(sender, **kwargs):
    """Ejecutar después de las migraciones"""
    if sender.name == 'gestion_calificaciones':
        # Crear usuarios admin si no existen
        if not Usuario.objects.filter(username='director').exists():
            Usuario.objects.create_user(
                username='director',
                password='director123',
                email='director@escuela63.edu.mx',
                tipo_usuario='admin'
            )
            print("✅ Usuario director creado")
        
        # Crear materias básicas
        materias = [
            {'nombre': 'Matemáticas', 'codigo': 'MAT001'},
            {'nombre': 'Español', 'codigo': 'ESP001'},
        ]
        
        for materia_data in materias:
            if not Materia.objects.filter(codigo=materia_data['codigo']).exists():
                Materia.objects.create(**materia_data)