from django.apps import AppConfig

class GestionCalificacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_calificaciones'

    def ready(self):
        import gestion_calificaciones.signals