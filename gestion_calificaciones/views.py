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
        user = self.request.user
        if user.tipo_usuario == 'estudiante':
            return Estudiante.objects.filter(usuario=user)
        return Estudiante.objects.all()

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