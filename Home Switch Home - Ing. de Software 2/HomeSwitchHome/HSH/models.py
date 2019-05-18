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


class Usuario(models.Model):
    email = models.EmailField(primary_key=True)
    contraseña = models.CharField(max_length=20)
    tarjeta_credito = models.CharField(max_length=16)
    creditos = models.PositiveSmallIntegerField()
    fecha_nac = models.DateField()
    nombre = models.CharField(max_length=25)


class Reserva(models.Model):
    id_residencia = models.ForeignKey(Residencia, on_delete=models.SET_DEFAULT, default='None')
    fecha = models.DateField()

    class Meta:
        unique_together = (("id_residencia", "fecha"),)


class Puja(models.Model):
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.FloatField()
