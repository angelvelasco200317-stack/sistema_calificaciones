from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from xhtml2pdf import pisa
import logging
from django.conf import settings
from .models import Estudiante, Calificacion, Materia

# Configurar logger
logger = logging.getLogger(__name__)

def generar_boleta_pdf(request, estudiante_id):
    try:
        # Validar que el estudiante existe
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        
        # Obtener nombre del estudiante (maneja tanto con usuario como sin usuario)
        if estudiante.usuario:
            nombre_completo = f"{estudiante.usuario.first_name} {estudiante.usuario.last_name}"
            # Separar en apellidos y nombres
            partes = nombre_completo.split()
            if len(partes) >= 2:
                apellido_paterno = partes[0] if len(partes) > 0 else ""
                apellido_materno = partes[1] if len(partes) > 1 else ""
                nombres = ' '.join(partes[2:]) if len(partes) > 2 else estudiante.usuario.first_name or ""
            else:
                apellido_paterno = estudiante.usuario.last_name or ""
                apellido_materno = ""
                nombres = estudiante.usuario.first_name or ""
        else:
            nombre_completo = estudiante.nombre_completo or ""
            # Separar nombre completo en partes
            partes = nombre_completo.split() if nombre_completo else []
            apellido_paterno = partes[0] if len(partes) > 0 else ""
            apellido_materno = partes[1] if len(partes) > 1 else ""
            nombres = ' '.join(partes[2:]) if len(partes) > 2 else nombre_completo
        
        # Obtener TODAS las calificaciones del estudiante
        calificaciones = Calificacion.objects.filter(
            estudiante=estudiante
        ).select_related('asignacion__materia')
        
        # Definir las materias según la boleta oficial
        materias_oficiales = [
            'Español',
            'Inglés',
            'Artes ',
            'Matemáticas',
            'Biología',
            'Geografía',
            'Historia',
            'Formación Cívica y Ética',
            'Educación Física',
            'Tecnología '
        ]
        
        # Organizar calificaciones
        calificaciones_organizadas = {}
        for materia_nombre in materias_oficiales:
            calificaciones_organizadas[materia_nombre] = {
                '1': '', '2': '', '3': '', 'final': ''
            }
        
        # Llenar con calificaciones reales
        for cal in calificaciones:
            try:
                # Obtener el nombre de la materia de la base de datos
                materia_db = cal.asignacion.materia
                materia_nombre_db = materia_db.get_nombre_display()
                
                # Mapeo de materias de la base de datos a materias oficiales
                mapeo_materias = {
    'espanol': 'Español',
    'ingles': 'Inglés',
    'artes': 'Artes',
    'matematicas': 'Matemáticas',
    'fisica': 'Biología',
    'quimica': 'Biología',
    'biologia': 'Biología',
    'geografia': 'Geografía',
    'historia': 'Historia',
    'formacion_civica': 'Formación Cívica y Ética',
    'educacion_fisica': 'Educación Física',
    'tecnologia': 'Tecnología',
}
                
                
                # Buscar materia correspondiente usando el código de la materia
                materia_codigo = materia_db.nombre  # Esto es el valor del choice
                materia_oficial = mapeo_materias.get(materia_codigo, materia_nombre_db)
                
                # Si no está en el mapeo, buscar por nombre similar
                if materia_oficial not in calificaciones_organizadas:
                    for materia_oficial_lista in materias_oficiales:
                        if materia_nombre_db.lower() in materia_oficial_lista.lower() or materia_oficial_lista.lower() in materia_nombre_db.lower():
                            materia_oficial = materia_oficial_lista
                            break
                
                if materia_oficial in calificaciones_organizadas:
                    try:
                        calificacion_float = float(cal.calificacion)
                        calificaciones_organizadas[materia_oficial][cal.periodo] = calificacion_float
                    except (ValueError, TypeError):
                        logger.warning(f"Calificación inválida para {materia_oficial}: {cal.calificacion}")
                        calificaciones_organizadas[materia_oficial][cal.periodo] = ''
                        
            except ObjectDoesNotExist:
                logger.error(f"Error en relación de objetos para calificación ID: {cal.id}")
                continue
            except Exception as e:
                logger.error(f"Error procesando calificación: {str(e)}")
                continue
        
        # Calcular promedios finales para cada materia
        for materia, califs in calificaciones_organizadas.items():
            calificaciones_validas = []
            
            for periodo in ['1', '2', '3']:
                if califs[periodo] != '':
                    calificaciones_validas.append(califs[periodo])
            
            if calificaciones_validas:
                promedio = sum(calificaciones_validas) / len(calificaciones_validas)
                calificaciones_organizadas[materia]['final'] = round(promedio, 2)
            else:
                calificaciones_organizadas[materia]['final'] = ''
        
        # Calcular promedio general del estudiante
        promedios_materias = []
        for materia, califs in calificaciones_organizadas.items():
            if califs['final'] != '':
                promedios_materias.append(califs['final'])
        
        promedio_general = ''
        if promedios_materias:
            promedio_general = round(sum(promedios_materias) / len(promedios_materias), 2)
        
        # Calcular total de inasistencias (esto es un ejemplo - ajusta según tu modelo)
        # Si tienes un modelo de Asistencia, aquí lo calcularías
        total_inasistencias = 0
        
        # Obtener URLs absolutas para los logos
        # Usar request.build_absolute_uri para obtener URLs completas
        base_url = request.build_absolute_uri('/')[:-1]  # Remover la última barra
        
        context = {
            'estudiante': estudiante,
            'nombre_completo': nombre_completo,
            'apellido_paterno': apellido_paterno,
            'apellido_materno': apellido_materno,
            'nombres': nombres,
            'calificaciones': calificaciones_organizadas,
            'ciclo_escolar': '2025-2026',
            'total_inasistencias': total_inasistencias,
            'promedio_general': promedio_general,
            'base_url': base_url,
        }
        
        # Cargar template con diseño oficial
        try:
            template = get_template('boleta_oficial.html')
            html = template.render(context)
        except Exception as e:
            logger.error(f"Error cargando template oficial: {str(e)}")
            # Si falla, intentar con template de backup
            try:
                logger.info("Intentando con template de backup...")
                template = get_template('admin/boleta_pdf.html.backup')
                html = template.render(context)
            except Exception as e2:
                logger.error(f"Error cargando template de backup: {str(e2)}")
                # Último recurso: HTML simple
                html = f"""
                <!DOCTYPE html>
                <html>
                <head><style>body {{ font-family: Arial; }}</style></head>
                <body>
                    <h1>Boleta de Calificaciones</h1>
                    <p><strong>Estudiante:</strong> {nombre_completo}</p>
                    <p><strong>Matrícula:</strong> {estudiante.matricula}</p>
                    <p><strong>Grado:</strong> {estudiante.grado} | <strong>Grupo:</strong> {estudiante.grupo}</p>
                    <p>Este es un documento temporal. Plantilla oficial no encontrada.</p>
                </body>
                </html>
                """
        
        response = HttpResponse(content_type='application/pdf')
        filename = f"BOLETA_{estudiante.matricula}_{estudiante.grado}{estudiante.grupo}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Generar PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            logger.error(f"Error generando PDF: {pisa_status.err}")
            return HttpResponse('Error al generar el archivo PDF', status=500)
            
        return response
        
    except Estudiante.DoesNotExist:
        logger.error(f"Estudiante no encontrado: {estudiante_id}")
        return HttpResponse('Estudiante no encontrado', status=404)
        
    except Exception as e:
        logger.error(f"Error inesperado en generar_boleta_pdf: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return HttpResponse('Error interno del servidor', status=500)

def reporte_grupo_pdf(request, grado, grupo):
    try:
        # Validar parámetros
        if not grado or not grupo:
            return HttpResponse('Grado y grupo son requeridos', status=400)
        
        # Obtener estudiantes con validación
        estudiantes = Estudiante.objects.filter(grado=grado, grupo=grupo)
        
        if not estudiantes.exists():
            return HttpResponse(f'No se encontraron estudiantes para {grado}° "{grupo}"', status=404)
        
        context = {
            'estudiantes': estudiantes,
            'grado': grado,
            'grupo': grupo,
            'ciclo_escolar': '2024-2025'
        }
        
        # Cargar template
        try:
            template = get_template('reporte_grupo_pdf.html')
            html = template.render(context)
        except Exception as e:
            logger.error(f"Error cargando template de grupo: {str(e)}")
            return HttpResponse('Error al cargar la plantilla del reporte', status=500)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="reporte_{grado}_{grupo}.pdf"'
        
        # Generar PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            logger.error(f"Error generando PDF de grupo: {pisa_status.err}")
            return HttpResponse('Error al generar el reporte PDF', status=500)
            
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en reporte_grupo_pdf: {str(e)}")
        return HttpResponse('Error interno del servidor', status=500)