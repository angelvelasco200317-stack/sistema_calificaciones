from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    ]
    
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO, default='estudiante')
    telefono = models.CharField(max_length=15, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # ELIMINA cualquier propiedad @property para is_staff
    # Deja que Django use el campo is_staff heredado de AbstractUser

    def save(self, *args, **kwargs):
        # Auto-asignar is_staff basado en el tipo de usuario al guardar
        if self.tipo_usuario == 'admin':
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)
    grado = models.CharField(max_length=10)
    grupo = models.CharField(max_length=5)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.matricula}"

class Docente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    numero_empleado = models.CharField(max_length=20, unique=True, default='temp_001')
    especialidad = models.CharField(max_length=100, default='General')

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.numero_empleado}"

class Asignacion(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    grado = models.CharField(max_length=10)
    grupo = models.CharField(max_length=5)
    ciclo_escolar = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.materia} - {self.grado}{self.grupo}"

class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=2, choices=[
        ('1', 'Primer Periodo'),
        ('2', 'Segundo Periodo'),
        ('3', 'Tercer Periodo'),
    ])
    calificacion = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    comentarios = models.TextField(blank=True)

    class Meta:
        unique_together = ['estudiante', 'asignacion', 'periodo']

    def __str__(self):
        return f"{self.estudiante} - {self.calificacion}"