from django.db import models
from django.db.models import Max, Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils import timezone

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
    activa = models.BooleanField(default=True)

    def borrar(self):
        self.activa = False
        reservas = Reserva.objects.filter(id_residencia=self)
        for res in reservas:
            subasta = Subasta.objects.get(id_reserva=res)
            if subasta.fecha_inicio > timezone.now().date() and subasta.esta_programada:
                subasta.delete()
                res.delete()
        self.save()

    def activada(self):
        return self.activa

class Usuario(models.Model):
    email = models.EmailField(primary_key=True)
    contraseña = models.CharField(max_length=20)
    tarjeta_credito = models.CharField(max_length=16)
    creditos = models.PositiveSmallIntegerField()
    fecha_nac = models.DateField()
    nombre = models.CharField(max_length=25)


class Reserva(models.Model):
    id_residencia = models.ForeignKey(Residencia, on_delete=models.CASCADE)
    fecha = models.DateField()

    class Meta:
        unique_together = (("id_residencia", "fecha"),)


class Subasta(models.Model):
    id = models.AutoField(primary_key=True)
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    esta_programada = models.BooleanField(default=True)

    def generar_monto(self):
        p = Puja()
        p.id_subasta=self
        p.id_usuario="xxxx@gmail.com"
        p.monto=0
        p.save()

    def obtener_monto_max(self):
        try:
            puja_max = Puja.objects.filter(id_subasta=self).aggregate(Max('monto'))
            return puja_max['monto__max']
        except ObjectDoesNotExist:
            return 0

class Puja(models.Model):
    id_subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE)
    id_usuario = models.EmailField()
    monto = models.FloatField()
