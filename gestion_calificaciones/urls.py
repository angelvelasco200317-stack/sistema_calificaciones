from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'materias', views.MateriaViewSet)
router.register(r'estudiantes', views.EstudianteViewSet)
router.register(r'docentes', views.DocenteViewSet)
router.register(r'asignaciones', views.AsignacionViewSet)
router.register(r'calificaciones', views.CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]