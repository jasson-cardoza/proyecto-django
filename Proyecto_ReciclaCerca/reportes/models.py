from django.db import models
from django.utils import timezone


class Reporte(models.Model):
    TIPOS = [
        ('punto_lleno', 'Punto de reciclaje lleno'),
        ('contenedor_danado', 'Contenedor dañado'),
        ('basura_acumulada', 'Basura acumulada'),
        ('sugerencia', 'Sugerencia'),
    ]
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('resuelto', 'Resuelto'),
    ]

    perfil = models.ForeignKey(
        'usuarios.Perfil', on_delete=models.CASCADE,
        related_name='reportes'
    )
    punto = models.ForeignKey(
        'reciclaje.PuntoReciclaje', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='reportes'
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.get_estado_display()}] {self.titulo}"

    # Método propio
    def marcar_resuelto(self):
        self.estado = 'resuelto'
        self.fecha_resolucion = timezone.now()
        self.save()

    # Método propio
    def esta_pendiente(self):
        return self.estado != 'resuelto'


class SeguimientoReporte(models.Model):
    reporte = models.ForeignKey(
        Reporte, on_delete=models.CASCADE, related_name='seguimientos'
    )
    autor = models.ForeignKey(
        'usuarios.Perfil', on_delete=models.CASCADE,
        related_name='seguimientos'
    )
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seguimiento de '{self.reporte.titulo}' por {self.autor.usuario.username}"

    # Método propio
    def resumen(self):
        return self.comentario[:50] + ('...' if len(self.comentario) > 50 else '')

