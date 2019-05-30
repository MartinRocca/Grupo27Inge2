from django import forms
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from HSH.models import Residencia, Puja, Subasta, Usuario
from datetime import datetime

class ResidenciaForm(forms.Form):
    localidad = forms.CharField()
    nombre = forms.CharField()
    descripcion = forms.CharField()
    precio_base = forms.FloatField()
    limite_personas = forms.IntegerField()
    cant_habitaciones = forms.IntegerField()
    nro_direccion = forms.IntegerField()
    calle = forms.CharField()
    imagen_URL = forms.URLField()

    def clean_cant_habitaciones(self):
        cant_habitaciones = self.cleaned_data.get('cant_habitaciones')
        if cant_habitaciones <= 0:
            raise forms.ValidationError("El número ingresado es inválido")
        return cant_habitaciones

    def clean_limite_personas(self):
        limite_personas = self.cleaned_data.get('limite_personas')
        if limite_personas <= 0:
            raise forms.ValidationError("El número ingresado es inválido")
        return limite_personas

    def clean_nro_direccion(self):
        nro_direccion = self.cleaned_data.get('nro_direccion')
        if nro_direccion <= 0:
            raise forms.ValidationError("El número ingresado es inválido")
        return nro_direccion

    def clean_precio_base(self):
        precio_base = self.cleaned_data.get('precio_base')
        if precio_base <= 0:
            raise forms.ValidationError("El número ingresado es inválido")
        return precio_base

    def save(self):
        r = Residencia()
        r.localidad = self.cleaned_data['localidad']
        r.nombre = self.cleaned_data['nombre']
        r.descripcion = self.cleaned_data['descripcion']
        r.precio_base = self.clean_precio_base()
        r.limite_personas = self.clean_limite_personas()
        r.nro_direccion = self.clean_nro_direccion()
        r.calle = self.cleaned_data['calle']
        r.cant_habitaciones = self.clean_cant_habitaciones()
        r.imagen_URL = self.cleaned_data['imagen_URL']
        r.save()
        return r

    def editar(self, id_residencia):
        r = Residencia.objects.get(id=id_residencia)
        r.localidad = self.cleaned_data['localidad']
        r.nombre = self.cleaned_data['nombre']
        r.descripcion = self.cleaned_data['descripcion']
        r.precio_base = self.clean_precio_base()
        r.limite_personas = self.clean_limite_personas()
        r.nro_direccion = self.clean_nro_direccion()
        r.calle = self.cleaned_data['calle']
        r.cant_habitaciones = self.clean_cant_habitaciones()
        r.imagen_URL = self.cleaned_data['imagen_URL']
        r.save()

class PujaForm(forms.Form):
    monto = forms.FloatField()


class RegistroForm(forms.Form):
    #email = forms.EmailField()
    #contraseña = forms.CharField()
    #nombre = forms.CharField()
    #fecha_nacimiento = forms.DateField()
    #nro_tarjeta_credito = forms.CharField()
    marca_tarjeta_credito = forms.CharField(widget=forms.RadioSelect(choices=[('VISA', 'Visa'), ('AMERICAN EXPRESS', 'American Express'), ('MASTERCARD', 'Mastercard')]))
    #nombre_titular_tarjeta = forms.CharField()
    #fecha_vencimiento_tarjeta = forms.DateField()
    #codigo_seguridad_tarjeta = forms.IntegerField(max_value=999)

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        edad = (datetime.now()-fecha).days/365
        if edad < 18:
            raise forms.ValidationError('Debes tener 18 años o mas de edad para registrarte.')
        return fecha

    def clean_nro_tarjeta_credito(self):
        n = self.cleaned_data.get('nro_tarjeta_credito')
        if len(str(n)) != 16:
            raise forms.ValidationError('El numero de tarjeta ingresado no es valido.')
        return n

    def clean_fecha_vencimiento_tarjeta(self):
        venc = self.cleaned_data.get('fecha_vencimiento_tarjeta')
        if venc < datetime.today():
            raise forms.ValidationError('La tarjeta ingresada esta vencida.')
        return venc

    def clean_codigo_seguridad_tarjeta(self):
        cod = self.cleaned_data.get('codigo_seguridad_tarjeta')
        if len(str(cod)) != 3:
            raise forms.ValidationError('El numero de seguridad ingresado no es valido.')
        return cod

    def save(self):
        u = Usuario()
        u.email = self.cleaned_data['email']
        u.contraseña = self.cleaned_data['contraseña']
        u.nombre = self.cleaned_data['nombre']
        u.fecha_nacimiento = self.clean_fecha_nacimiento()
        u.nro_tarjeta_credito = self.clean_nro_tarjeta_credito()
        u.marca_tarjeta_credito = self.cleaned_data['marca_tarjeta_credito']
        u.nombre_titular_tarjeta = self.cleaned_data['nombre_titular_tarjeta']
        u.fecha_vencimiento_tarjeta = self.clean_fecha_vencimiento_tarjeta()
        u.codigo_seguridad_tarjeta = self.clean_codigo_seguridad_tarjeta()
        u.save()