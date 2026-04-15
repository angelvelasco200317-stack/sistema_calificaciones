from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.http import JsonResponse
from gestion_calificaciones import views, reports  
from gestion_calificaciones.admin import admin_site

router = routers.DefaultRouter()
router.register(r'materias', views.MateriaViewSet)
router.register(r'estudiantes', views.EstudianteViewSet)
router.register(r'docentes', views.DocenteViewSet)
router.register(r'asignaciones', views.AsignacionViewSet)
router.register(r'calificaciones', views.CalificacionViewSet)

def api_root(request):
    return JsonResponse({
        'message': 'Sistema de Gestión de Calificaciones - Escuela Secundaria Técnica N°63',
        'endpoints': {
            'materias': '/api/materias/',
            'estudiantes': '/api/estudiantes/',
            'docentes': '/api/docentes/',
            'asignaciones': '/api/asignaciones/',
            'calificaciones': '/api/calificaciones/',
            'boleta_pdf': '/api/boleta/<id>/pdf/',
            'reporte_grupo': '/api/grupo/<grado>/<grupo>/reporte/',
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', api_root),
    path('admin/', admin_site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    
    # 👇 RUTAS DIRECTAS DE REPORTES PDF
    path('api/boleta/<int:estudiante_id>/pdf/', reports.generar_boleta_pdf, name='generar_boleta_pdf'),  
    path('api/grupo/<str:grado>/<str:grupo>/reporte/', reports.reporte_grupo_pdf, name='reporte_grupo_pdf'),  
]