from django.core.exceptions import ValidationError
from django.db import models, transaction

class Material(models.Model):
    CATEGORIAS = [
        ('plastico', 'Plástico'),
        ('papel', 'Papel y cartón'),
        ('vidrio', 'Vidrio'),
        ('metal', 'Metal'),
        ('electronico', 'Electrónico'),
        ('organico', 'Orgánico'),
    ]

    nombre = models.CharField(max_length=80, unique=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    descripcion = models.TextField(blank=True)
    puntos_por_kg = models.PositiveIntegerField(default=10)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

    # Método propio
    def calcular_puntos(self, kilos):
        return int(self.puntos_por_kg * kilos)


class PuntoReciclaje(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15, blank=True)
    horario = models.CharField(max_length=100, blank=True)
    materiales_aceptados = models.ManyToManyField(
        Material, related_name='puntos', blank=True
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.municipio}"

    # Método propio
    def acepta_material(self, material):
        return self.materiales_aceptados.filter(pk=material.pk).exists()


class RegistroReciclaje(models.Model):
    perfil = models.ForeignKey(
        'usuarios.Perfil', on_delete=models.CASCADE,
        related_name='reciclajes'
    )
    punto = models.ForeignKey(
        PuntoReciclaje, on_delete=models.PROTECT,
        related_name='registros'
    )
    material = models.ForeignKey(
        Material, on_delete=models.PROTECT,
        related_name='registros'
    )
    cantidad_kg = models.DecimalField(max_digits=7, decimal_places=2)
    puntos_ganados = models.PositiveIntegerField(default=0, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.perfil.usuario.username}: {self.cantidad_kg} kg de {self.material.nombre}"

    # Método propio
    def calcular_puntos(self):
        return self.material.calcular_puntos(self.cantidad_kg)

    # Método propio
    def _validar_reglas(self):
        """Reglas de negocio del registro. Lanza ValidationError si no se cumplen."""
        if self.cantidad_kg is None or self.cantidad_kg <= 0:
            raise ValidationError(
                {'cantidad_kg': 'La cantidad debe ser mayor que 0.'}
            )
        # Solo al crear: un punto puede dejar de aceptar un material más
        # adelante y eso no debe invalidar los registros antiguos.
        if self.pk is None and self.punto_id and self.material_id:
            if not self.punto.acepta_material(self.material):
                raise ValidationError({
                    'material': f"El punto '{self.punto.nombre}' no acepta "
                                f"{self.material.nombre}."
                })

    def clean(self):
        # Lo usan el panel de administración y los formularios.
        super().clean()
        if self.cantidad_kg is not None:
            self._validar_reglas()

    def save(self, *args, **kwargs):
        # Lo usa el código en general (vistas, shell, scripts): valida igual.
        self._validar_reglas()
        es_nuevo = self.pk is None
        # Atómico: el registro y los puntos del perfil se guardan juntos o no se guarda nada.
        with transaction.atomic():
            if es_nuevo:
                self.puntos_ganados = self.calcular_puntos()
            super().save(*args, **kwargs)
            if es_nuevo:
                self.perfil.sumar_puntos(self.puntos_ganados)
# Create your models here.
