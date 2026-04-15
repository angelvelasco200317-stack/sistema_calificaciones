from django.core.management.base import BaseCommand
from gestion_calificaciones.models import Usuario

class Command(BaseCommand):
    help = 'Inicializar datos básicos del sistema'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Inicializando datos del sistema...')
        
        # Crear usuarios admin
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
        ]
        
        for usuario_data in usuarios:
            if not Usuario.objects.filter(username=usuario_data['username']).exists():
                usuario = Usuario.objects.create_user(**usuario_data)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Usuario {usuario.username} creado')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Usuario {usuario_data["username"]} ya existe')
                )
        
        self.stdout.write(self.style.SUCCESS('🎉 Inicialización completada!'))