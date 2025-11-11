from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Materia, Estudiante, Docente, Asignacion, Calificacion

# Personalizar el AdminSite para eliminar acciones recientes
class MyAdminSite(admin.AdminSite):
    site_header = 'Sistema de Calificaciones'
    site_title = 'Administración del Sistema'
    index_title = 'Panel de Control'
    
    def get_app_list(self, request, app_label=None):
        """
        Devuelve la lista de aplicaciones sin el panel de acciones recientes
        """
        app_list = super().get_app_list(request, app_label)
        return app_list

# Crear instancia del admin site personalizado
admin_site = MyAdminSite(name='myadmin')

# Custom User Admin para el modelo Usuario personalizado
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'telefono', 'tipo_usuario')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'fecha_creacion')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'tipo_usuario', 'email', 'first_name', 'last_name'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff', 'is_active')
    list_filter = ('tipo_usuario', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

# Admin para Estudiante
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'usuario', 'grado', 'grupo', 'fecha_inscripcion')
    list_filter = ('grado', 'grupo')
    search_fields = ('matricula', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    raw_id_fields = ('usuario',)

# Admin para Docente
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'usuario', 'especialidad')
    search_fields = ('numero_empleado', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    raw_id_fields = ('usuario',)

# Admin para Asignacion
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('materia', 'docente', 'grado', 'grupo', 'ciclo_escolar')
    list_filter = ('grado', 'grupo', 'ciclo_escolar', 'materia')
    search_fields = ('materia__nombre', 'docente__usuario__first_name', 'docente__usuario__last_name')
    raw_id_fields = ('docente', 'materia')

# Admin para Calificacion
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'asignacion', 'periodo', 'calificacion', 'fecha_registro')
    list_filter = ('periodo', 'asignacion__materia', 'asignacion__grado')
    search_fields = ('estudiante__usuario__first_name', 'estudiante__usuario__last_name', 'estudiante__matricula')
    raw_id_fields = ('estudiante', 'asignacion')

# Admin para Materia
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'codigo')

# Registrar todos los modelos con el admin site personalizado
admin_site.register(Usuario, CustomUserAdmin)
admin_site.register(Materia, MateriaAdmin)
admin_site.register(Estudiante, EstudianteAdmin)
admin_site.register(Docente, DocenteAdmin)
admin_site.register(Asignacion, AsignacionAdmin)
admin_site.register(Calificacion, CalificacionAdmin)

# También registrar los modelos de auth si los necesitas
from django.contrib.auth.models import Group
admin_site.register(Group)