from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Materia, Estudiante, Docente, Asignacion, Calificacion
from .serializers import *

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.tipo_usuario == 'admin'

class IsDocenteOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario in ['docente', 'admin']

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [IsAdminOrReadOnly]



class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Estudiante.objects.all()
        user = self.request.user
        
        # Filtrar por grado si se proporciona
        grado = self.request.query_params.get('grado')
        if grado:
            queryset = queryset.filter(grado=grado)
            
        # Filtrar por grupo si se proporciona
        grupo = self.request.query_params.get('grupo')
        if grupo:
            queryset = queryset.filter(grupo=grupo)
            
        # Si es estudiante, solo ver su propio registro
        if user.tipo_usuario == 'estudiante':
            try:
                queryset = queryset.filter(usuario=user)
            except Estudiante.DoesNotExist:
                queryset = queryset.none()
                
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_grupo(self, request):
        """Obtener todos los estudiantes de un grupo específico"""
        grado = request.query_params.get('grado')
        grupo = request.query_params.get('grupo')
        
        if not grado or not grupo:
            return Response(
                {'error': 'Se requieren los parámetros grado y grupo'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        estudiantes = Estudiante.objects.filter(grado=grado, grupo=grupo)
        serializer = self.get_serializer(estudiantes, many=True)
        
        # Agregar estadísticas
        total = estudiantes.count()
        con_usuario = estudiantes.filter(usuario__isnull=False).count()
        sin_usuario = total - con_usuario
        
        return Response({
            'estudiantes': serializer.data,
            'estadisticas': {
                'total': total,
                'con_usuario': con_usuario,
                'sin_usuario': sin_usuario
            }
        })
    
    @action(detail=False, methods=['post'])
    def importar_grupo(self, request):
        """Importar múltiples estudiantes para un grupo"""
        grado = request.data.get('grado')
        grupo = request.data.get('grupo')
        estudiantes_data = request.data.get('estudiantes', [])
        
        if not grado or not grupo:
            return Response(
                {'error': 'Se requieren grado y grupo'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        estudiantes_creados = []
        for estudiante_data in estudiantes_data:
            # Generar matrícula única
            matricula_base = f"{grado}{grupo}{str(len(estudiantes_creados) + 1).zfill(3)}"
            matricula = matricula_base
            
            # Verificar que la matrícula no exista
            counter = 1
            while Estudiante.objects.filter(matricula=matricula).exists():
                matricula = f"{matricula_base}-{counter}"
                counter += 1
            
            estudiante = Estudiante.objects.create(
                matricula=matricula,
                nombre_completo=estudiante_data.get('nombre_completo'),
                grado=grado,
                grupo=grupo,
                email_contacto=estudiante_data.get('email_contacto'),
                telefono_contacto=estudiante_data.get('telefono_contacto')
            )
            estudiantes_creados.append(estudiante)
        
        serializer = self.get_serializer(estudiantes_creados, many=True)
        return Response({
            'mensaje': f'Se importaron {len(estudiantes_creados)} estudiantes',
            'estudiantes': serializer.data
        })
class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.tipo_usuario == 'docente':
            return Docente.objects.filter(usuario=user)
        return Docente.objects.all()

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    permission_classes = [IsDocenteOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.tipo_usuario == 'docente':
            docente = Docente.objects.get(usuario=user)
            return Asignacion.objects.filter(docente=docente)
        return Asignacion.objects.all()

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsDocenteOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.tipo_usuario == 'docente':
            docente = Docente.objects.get(usuario=user)
            asignaciones = Asignacion.objects.filter(docente=docente)
            return Calificacion.objects.filter(asignacion__in=asignaciones)
        elif user.tipo_usuario == 'estudiante':
            estudiante = Estudiante.objects.get(usuario=user)
            return Calificacion.objects.filter(estudiante=estudiante)
        return Calificacion.objects.all()

    @action(detail=False, methods=['get'])
    def mis_calificaciones(self, request):
        if request.user.tipo_usuario == 'estudiante':
            try:
                estudiante = Estudiante.objects.get(usuario=request.user)
                calificaciones = Calificacion.objects.filter(estudiante=estudiante)
                serializer = self.get_serializer(calificaciones, many=True)
                return Response(serializer.data)
            except Estudiante.DoesNotExist:
                return Response([])
        return Response({'error': 'No autorizado'}, status=403)