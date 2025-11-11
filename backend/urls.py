from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.http import JsonResponse
from gestion_calificaciones import views
from gestion_calificaciones.admin import admin_site  # 👈 AGREGAR esta línea

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
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', api_root),
    path('admin/', admin_site.urls),  # 👈 CAMBIAR esta línea (admin.site.urls → admin_site.urls)
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]