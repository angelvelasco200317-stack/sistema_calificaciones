import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from gestion_calificaciones.models import Estudiante

def importar_grupo_completo(grado, grupo, estudiantes_data):
    """
    Importa un grupo completo de estudiantes
    estudiantes_data: Lista de diccionarios con nombre_completo, email, telefono
    """
    resultados = []
    
    for i, estudiante_info in enumerate(estudiantes_data, 1):
        # Generar matrícula secuencial
        matricula = f"{grado}{grupo}{str(i).zfill(3)}"
        
        # Crear estudiante sin usuario
        estudiante = Estudiante.objects.create(
            matricula=matricula,
            nombre_completo=estudiante_info['nombre_completo'],
            grado=grado,
            grupo=grupo,
            email_contacto=estudiante_info.get('email', ''),
            telefono_contacto=estudiante_info.get('telefono', '')
        )
        
        resultados.append({
            'matricula': estudiante.matricula,
            'nombre': estudiante.nombre_completo,
            'estado': 'Creado'
        })
        print(f"✅ Estudiante creado: {estudiante.nombre_completo} ({matricula})")
    
    return resultados

# Ejemplo de uso
if __name__ == '__main__':
    # Datos de ejemplo para el grupo 1-A
    estudiantes_1A = [
        {'nombre_completo': 'Juan Pérez Hernández', 'email': 'juan@escuela63.edu.mx'},
        {'nombre_completo': 'María García López', 'email': 'maria@escuela63.edu.mx'},
        {'nombre_completo': 'Carlos Rodríguez Silva', 'email': 'carlos@escuela63.edu.mx'},
    ]
    
    resultados = importar_grupo_completo('1', 'A', estudiantes_1A)
    print(f"\n🎯 Total creados: {len(resultados)} estudiantes")