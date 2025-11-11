from rest_framework import serializers
from .models import Usuario, Materia, Estudiante, Docente, Asignacion, Calificacion

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo_usuario']

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

class EstudianteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = '__all__'

class DocenteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Docente
        fields = '__all__'

class AsignacionSerializer(serializers.ModelSerializer):
    docente = DocenteSerializer(read_only=True)
    materia = MateriaSerializer(read_only=True)
    
    class Meta:
        model = Asignacion
        fields = '__all__'

class CalificacionSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer(read_only=True)
    asignacion = AsignacionSerializer(read_only=True)
    
    class Meta:
        model = Calificacion
        fields = '__all__'