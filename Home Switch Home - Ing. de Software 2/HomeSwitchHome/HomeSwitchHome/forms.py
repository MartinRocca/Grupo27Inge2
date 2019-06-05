from django import forms
from django.contrib.auth.forms import UserCreationForm
from HSH.models import Residencia, Puja, Subasta, Perfil, Usuario
from datetime import datetime
from django.core.validators import RegexValidator
from django.utils.translation import gettext, gettext_lazy as _

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

class RegistroForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = [
            'email',
        ]

    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, max_length=50, strip=False)
    password2 = forms.CharField(label='Repita su contraseña', widget=forms.PasswordInput, max_length=50, strip=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            coincidencia = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return email
        raise forms.ValidationError('Este mail ya se encuentra en uso.')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

class PerfilForm(forms.Form):

    nombre = forms.CharField(label='Nombre', max_length=50)
    apellido = forms.CharField(label='Apellido', max_length=50)
    fecha_nacimiento = forms.DateField(
        label='Fecha de nacimiento (formato DD/MM/AA)',
        input_formats=["%d/%m/%y"],
        error_messages={'invalid': 'Ingrese una fecha valida.'}
    )
    nro_tarjeta_credito = forms.CharField(
        label='Numero de tarjeta de credito',
        max_length=16,
        min_length=16,
        validators=[RegexValidator('^[0-9]*$', message='Solo se aceptan caracteres numericos.')]
    )
    marca_tarjeta_credito = forms.CharField(
        label='Marca de tarjeta de credito',
        widget=forms.RadioSelect(
            choices=[
                ('VISA', 'Visa'),
                ('AMERICAN EXPRESS', 'American Express'),
                ('MASTERCARD', 'Mastercard')
            ]
        )
    )
    nombre_titular_tarjeta = forms.CharField(label='Nombre del titular', max_length=120)
    fecha_vencimiento_tarjeta = forms.DateField(
        label='Fecha de vencimiento (formato DD/MM/AA)',
        input_formats=["%d/%m/%y"],
        error_messages={'invalid': 'Ingrese una fecha valida.'}
    )
    codigo_seguridad_tarjeta = forms.CharField(
        label='Codigo de seguridad',
        max_length=3,
        min_length=3,
        validators=[RegexValidator('^[0-9]*$', message='Solo se aceptan caracteres numericos.')]
    )

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        edad = (datetime.now().date() - fecha).days / 365
        if edad < 18:
            raise forms.ValidationError('Debes tener 18 años o mas de edad para registrarte.')
        return fecha

    def clean_fecha_vencimiento_tarjeta(self):
        venc = self.cleaned_data.get('fecha_vencimiento_tarjeta')
        if venc < datetime.today().date():
            raise forms.ValidationError('La tarjeta ingresada esta vencida.')
        return venc

    def save(self):
        p = Perfil()
        p.nombre = self.cleaned_data.get('nombre')
        p.apellido = self.cleaned_data.get('apellido')
        p.fecha_nacimiento = self.clean_fecha_nacimiento()
        p.nro_tarjeta_credito = self.cleaned_data.get('nro_tarjeta_credito')
        p.marca_tarjeta_credito = self.cleaned_data.get('marca_tarjeta_credito')
        p.nombre_titular_tarjeta = self.cleaned_data.get('nombre_titular_tarjeta')
        p.fecha_vencimiento_tarjeta = self.clean_fecha_vencimiento_tarjeta()
        p.codigo_seguridad_tarjeta = self.cleaned_data.get('codigo_seguridad_tarjeta')
        p.save()
        return p