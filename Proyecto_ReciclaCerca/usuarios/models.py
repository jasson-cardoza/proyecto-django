from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    TIPO_USUARIO = [
        ('ciudadano', 'Ciudadano'),
        ('recolector', 'Recolector'),
        ('empresa', 'Empresa recicladora'),
    ]

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil'
    )
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo_usuario = models.CharField(
        max_length=20, choices=TIPO_USUARIO, default='ciudadano'
    )
    puntos = models.PositiveIntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.get_tipo_usuario_display()})"


    def sumar_puntos(self, cantidad):
        self.puntos += cantidad
        self.save()
        return self.puntos

    # Método propio
    def nombre_completo(self):
        return self.usuario.get_full_name() or self.usuario.username


class Direccion(models.Model):
    perfil = models.ForeignKey(
        Perfil, on_delete=models.CASCADE, related_name='direcciones'
    )
    departamento = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    detalle = models.CharField(max_length=200)
    es_principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.municipio}, {self.departamento}"


    def direccion_completa(self):
        return f"{self.detalle}, {self.municipio}, {self.departamento}"


# Create your models here.
