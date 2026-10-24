from django.db import models

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

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        if es_nuevo:
            self.puntos_ganados = self.calcular_puntos()
        super().save(*args, **kwargs)
        if es_nuevo:
            self.perfil.sumar_puntos(self.puntos_ganados)
# Create your models here.
