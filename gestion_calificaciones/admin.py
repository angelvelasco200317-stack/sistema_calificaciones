from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Materia, Estudiante, Docente, Asignacion, Calificacion

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

admin_site = MyAdminSite(name='myadmin')

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name', 'email', 'telefono', 'tipo_usuario')}),
        (_('Permisos'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}), 
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'tipo_usuario', 'email', 'first_name', 'last_name'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff', 'is_active', 'fecha_creacion')
    list_filter = ('tipo_usuario', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    
    readonly_fields = ('fecha_creacion', 'last_login', 'date_joined')


class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'get_nombre', 'grado', 'grupo', 'fecha_inscripcion', 'tiene_usuario', 'acciones_boleta')
    
    
    list_filter = ('grado', 'grupo', 'usuario')  
    
    class TieneUsuarioFilter(admin.SimpleListFilter):
        title = 'tiene usuario'
        parameter_name = 'tiene_usuario'
        
        def lookups(self, request, model_admin):
            return (
                ('si', 'Con usuario'),
                ('no', 'Sin usuario'),
            )
        
        def queryset(self, request, queryset):
            if self.value() == 'si':
                return queryset.filter(usuario__isnull=False)
            if self.value() == 'no':
                return queryset.filter(usuario__isnull=True)
    
    list_filter = ('grado', 'grupo', TieneUsuarioFilter)
    
    search_fields = ('matricula', 'nombre_completo', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    raw_id_fields = ('usuario',)
    
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('matricula', 'nombre_completo', 'grado', 'grupo')
        }),
        ('Información de Contacto', {
            'fields': ('email_contacto', 'telefono_contacto'),
            'classes': ('collapse',)
        }),
        ('Usuario del Sistema (Opcional)', {
            'fields': ('usuario',),
            'description': 'Asociar a un usuario existente del sistema'
        }),
    )
    
    def get_nombre(self, obj):
        if obj.usuario:
            return obj.usuario.get_full_name()
        return obj.nombre_completo or "Sin nombre"
    get_nombre.short_description = 'Nombre'
    get_nombre.admin_order_field = 'nombre_completo'
    
    def tiene_usuario(self, obj):
        return obj.usuario is not None
    tiene_usuario.boolean = True
    tiene_usuario.short_description = 'Tiene usuario'
    
    def acciones_boleta(self, obj):
        if not obj.usuario:
            return "Primero asocia un usuario"
        return format_html(
            '<a class="button" href="/api/boleta/{}/pdf/" target="_blank" style="background-color: #4CAF50; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; font-size: 12px; display: inline-block; margin: 2px;">Boleta PDF</a>&nbsp;'
            '<a class="button" href="/admin/gestion_calificaciones/calificacion/?estudiante__id__exact={}" style="background-color: #2196F3; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; font-size: 12px; display: inline-block; margin: 2px;">Ver Calificaciones</a>',
            obj.id, obj.id
        )
    acciones_boleta.short_description = 'Acciones Rápidas'   

class DocenteAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'usuario', 'especialidad')
    search_fields = ('numero_empleado', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    raw_id_fields = ('usuario',)

class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('materia', 'docente', 'grado', 'grupo', 'ciclo_escolar')
    list_filter = ('grado', 'grupo', 'ciclo_escolar', 'materia')
    search_fields = ('materia__nombre', 'docente__usuario__first_name', 'docente__usuario__last_name')
    raw_id_fields = ('docente', 'materia')

class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'asignacion', 'periodo', 'calificacion', 'fecha_registro', 'acciones_rapidas')
    list_filter = ('periodo', 'asignacion__materia', 'asignacion__grado')
    search_fields = ('estudiante__usuario__first_name', 'estudiante__usuario__last_name', 'estudiante__matricula')
    raw_id_fields = ('estudiante', 'asignacion')
    
    def acciones_rapidas(self, obj):
        return format_html(
            '<a class="button" href="/api/boleta/{}/pdf/" target="_blank" style="background-color: #FF9800; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; font-size: 12px; display: inline-block; margin: 2px;">📄 Boleta Estudiante</a>',
            obj.estudiante.id
        )
    acciones_rapidas.short_description = 'Acciones'

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'codigo')

admin_site.register(Usuario, CustomUserAdmin)
admin_site.register(Materia, MateriaAdmin)
admin_site.register(Estudiante, EstudianteAdmin)
admin_site.register(Docente, DocenteAdmin)
admin_site.register(Asignacion, AsignacionAdmin)
admin_site.register(Calificacion, CalificacionAdmin)


from django.contrib.auth.models import Group
admin_site.register(Group)