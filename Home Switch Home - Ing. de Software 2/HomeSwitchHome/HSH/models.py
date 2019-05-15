from django.db import models


# Create your models here.

class Residencia(models.Model):
    localidad = models.CharField(max_length=150)
    nombre = models.CharField(max_length=70)
    descripcion = models.TextField()
    precio_base = models.FloatField()
    limite_personas = models.PositiveSmallIntegerField()
    nro_direccion = models.PositiveIntegerField()
    calle = models.CharField(max_length=100)
    cant_habitaciones = models.PositiveSmallIntegerField()
    imagen_URL = models.URLField()

    class Meta:
        unique_together = (("localidad", "nro_direccion", "calle"),)