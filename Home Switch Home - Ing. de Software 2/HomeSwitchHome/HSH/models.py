from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.dispatch import receiver


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
    usuario_ganador = models.EmailField(null=True)


    def reservar(self, mailUsuario):
        subasta = Subasta.objects.get(id_reserva=self)
        subasta.esta_programada = False
        subasta.save()
        self.set_ganador(mailUsuario)

    def set_ganador(self, mailUsuario):
        self.usuario_ganador = mailUsuario
        self.save()
        perfil_ganador = Usuario.objects.get(email=mailUsuario).get_perfil()
        perfil_ganador.creditos = perfil_ganador.creditos - 1
        perfil_ganador.save()


    class Meta:
        unique_together = (("id_residencia", "fecha"),)

class Subasta(models.Model):
    id = models.AutoField(primary_key=True)
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    esta_programada = models.BooleanField(default=True)


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
            while True:
                if puja_ganadora.id_usuario.get_perfil().creditos >= 1:
                    self.id_reserva.set_ganador(puja_ganadora.id_usuario)
                    self.esta_programada = False
                    self.save()
                    break
                else:
                    Puja.objects.filter(id_subasta=self).latest('monto').delete()
                    puja_ganadora = Puja.objects.filter(id_subasta=self).latest('monto')
            return puja_ganadora.id_usuario
        except:
            return "-"

    def cerrar_subasta(self):
        self.obtener_ganador()
        self.esta_programada=False
        self.save()

    def cancelar_subasta(self):
        try:
            self.esta_programada = False
            Puja.objects.filter(id_subasta=self).delete()
            self.save()
        except:
            pass

class Puja(models.Model):
    id_subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE)
    id_usuario = models.EmailField()
    monto = models.FloatField()

class Perfil(models.Model):
    mi_usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null=True)
    nro_tarjeta_credito = models.IntegerField(null=True)
    marca_tarjeta_credito = models.CharField(max_length=30)
    nombre_titular_tarjeta = models.CharField(max_length=120)
    fecha_vencimiento_tarjeta = models.DateField(null=True)
    codigo_seguridad_tarjeta = models.IntegerField(null=True)
    creditos = models.IntegerField(default=2)
    vencimiento_creditos = models.DateField(null=True)

    class meta:
        unique_together = ('nombre', 'apellido')

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Se necesita un email.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault((('is_superuser', False),('is_admin', False),('mi_perfil', None)))
        return self._create_user(email,password,**extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_premium = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_premium = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_perfil(self):
        try:
            return Perfil.objects.get(mi_usuario=self)
        except ObjectDoesNotExist:
            return None


class Precio(models.Model):
    precio_Normal = models.FloatField()
    precio_Premium = models.FloatField()

    def editar_precio(self, unPrecioNormal, unPrecioPremium):
        self.precio_Normal = unPrecioNormal
        self.precio_Premium = unPrecioPremium
        self.save()