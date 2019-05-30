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
            elif subasta.esta_programada:
                subasta.cancelar_subasta()
        self.save()

    def activada(self):
        return self.activa

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

    # hay que ver como hacer bien lo del premium, se podria agregar un campo más.

    def obtener_monto_max(self):
        try:
            puja_max = Puja.objects.filter(id_subasta=self).aggregate(Max('monto'))
            if puja_max['monto__max'] is None:
                return self.id_reserva.id_residencia.precio_base
            else:
                return puja_max['monto__max']
        except ObjectDoesNotExist:
            return self.id_reserva.id_residencia.precio_base

    def obtener_ganador(self):
        try:
            puja_ganadora = Puja.objects.filter(id_subasta=self).latest('monto')
            return puja_ganadora.id_usuario
        except:
            return "-"

    def cerrar_subasta(self):
        try:
            self.esta_programada = False
            self.save()
            # más adelante habría que verificar si el usuario tiene créditos y si es el caso, descontarle 1.
        except:
            pass

    def cancelar_subasta(self):
        try:
            self.esta_programada = False
            Puja.objects.filter(id_subasta=self).delete()
            self.save()
            # más adelante habría que verificar si el usuario tiene créditos y si es el caso, descontarle 1.
        except:
            pass

class Puja(models.Model):
    id_subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE)
    id_usuario = models.EmailField()
    monto = models.FloatField()

class Usuario(models.Model):
    email = models.EmailField(primary_key=True)
    contraseña = models.CharField(max_length=20)
    nombre = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    nro_tarjeta_credito = models.PositiveIntegerField()
    marca_tarjeta_credito = models.CharField(max_length= 20, choices=[('VISA', 'Visa'), ('AMERICAN EXPRESS', 'American Express'), ('MASTERCARD', 'Mastercard')])
    nombre_titular_tarjeta = models.CharField(max_length=30)
    fecha_vencimiento_tarjeta = models.DateField()
    codigo_seguridad_tarjeta = models.PositiveIntegerField()

    creditos = models.IntegerField(default=2)
    es_premium = models.BooleanField(default=False)
