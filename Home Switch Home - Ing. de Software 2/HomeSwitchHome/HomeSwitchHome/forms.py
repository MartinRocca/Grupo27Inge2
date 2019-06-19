from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Por favor ingrese un email y contraseña validos. "
            "Note que ambos campos diferencian entre mayusculas y minusculas."
        ),
        'inactive': _("Esta cuenta fue borrada.")
    }

class PerfilForm(forms.Form):

    nombre = forms.CharField(label='Nombre', max_length=50)
    apellido = forms.CharField(label='Apellido', max_length=50)
    fecha_nacimiento = forms.DateField(
        label='Fecha de nacimiento (formato Dia/Mes/Año)',
        input_formats=[
            "%d/%m/%y",
            "%D/%m/%y",
            "%d/%M/%y",
            "%d/%m/%Y",
            "%D/%M/%y",
            "%D/%m/%Y",
            "%d/%M/%Y",
            "%D/%M/%Y"
        ],
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
                ('Visa', 'Visa'),
                ('American Express', 'American Express'),
                ('Mastercard', 'Mastercard')
            ]
        )
    )
    nombre_titular_tarjeta = forms.CharField(label='Nombre del titular', max_length=120)
    fecha_vencimiento_tarjeta = forms.DateField(
        label='Fecha de vencimiento (formato DD/MM/AA)',
        input_formats=["%d/%m/%y","%D/%M/&y"],
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
        edad = (datetime.now().date() - fecha).days / 365.24
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

class EditarPerfilForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50)
    apellido = forms.CharField(label='Apellido', max_length=50)
    fecha_nacimiento = forms.DateField(
        label='Fecha de nacimiento (formato Dia/Mes/Año)',
        input_formats=[
            "%d/%m/%y",
            "%D/%m/%y",
            "%d/%M/%y",
            "%d/%m/%Y",
            "%D/%M/%y",
            "%D/%m/%Y",
            "%d/%M/%Y",
            "%D/%M/%Y"
        ],
        error_messages={'invalid': 'Ingrese una fecha valida.'}
    )

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        edad = (datetime.now().date() - fecha).days / 365.24
        if edad < 18:
            raise forms.ValidationError('Debes tener 18 años o mas para utilizar el sitio HomeSwitchHome.')
        return fecha

    def editar(self, id_perfil):
        p = Perfil.objects.get(id=id_perfil)
        p.nombre = self.cleaned_data.get('nombre')
        p.apellido = self.cleaned_data.get('apellido')
        p.fecha_nacimiento = self.clean_fecha_nacimiento()
        p.save()

class CambiarTarjetaForm(forms.Form):
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
                ('Visa', 'Visa'),
                ('American Express', 'American Express'),
                ('Mastercard', 'Mastercard')
            ]
        )
    )
    nombre_titular_tarjeta = forms.CharField(label='Nombre del titular', max_length=120)
    fecha_vencimiento_tarjeta = forms.DateField(
        label='Fecha de vencimiento (formato DD/MM/AA)',
        input_formats=["%d/%m/%y", "%D/%M/&y"],
        error_messages={'invalid': 'Ingrese una fecha valida.'}
    )
    codigo_seguridad_tarjeta = forms.CharField(
        label='Codigo de seguridad',
        max_length=3,
        min_length=3,
        validators=[RegexValidator('^[0-9]*$', message='Solo se aceptan caracteres numericos.')]
    )

    def clean_fecha_vencimiento_tarjeta(self):
        venc = self.cleaned_data.get('fecha_vencimiento_tarjeta')
        if venc < datetime.today().date():
            raise forms.ValidationError('La tarjeta ingresada esta vencida.')
        return venc

    def editar(self, id_perfil):
        p = Perfil.objects.get(id=id_perfil)
        p.nro_tarjeta_credito = self.cleaned_data.get('nro_tarjeta_credito')
        p.marca_tarjeta_credito = self.cleaned_data.get('marca_tarjeta_credito')
        p.nombre_titular_tarjeta = self.cleaned_data.get('nombre_titular_tarjeta')
        p.fecha_vencimiento_tarjeta = self.clean_fecha_vencimiento_tarjeta()
        p.codigo_seguridad_tarjeta = self.cleaned_data.get('codigo_seguridad_tarjeta')
        p.save()

class PrecioForm(forms.Form):
    precio_Normal = forms.FloatField()
    precio_Premium = forms.FloatField()

    def clean_precio_Normal(self):
        pNormal = self.cleaned_data.get('precio_Normal')
        if pNormal < 0:
            raise forms.ValidationError('Valor inválido')
        return pNormal

    def clean_precio_Premium(self):
        pPremium = self.cleaned_data.get('precio_Premium')
        if pPremium < 0:
            raise forms.ValidationError('Valor inválido')
        return pPremium

class BuscarResidenciasForm(forms.Form):
    lugar = forms.CharField(label='Ingrese una localidad', required=False)
    fecha_desde = forms.DateField(
        label='Fecha desde (formato DD/MM/AA)',
        input_formats=["%d/%m/%y", "%D/%M/%y"],
        error_messages={'invalid': 'Ingrese una fecha valida.'}, required=False
    )
    fecha_hasta = forms.DateField(
        label='Fecha hasta (formato DD/MM/AA)',
        input_formats=["%d/%m/%y", "%D/%M/%y"],
        error_messages={'invalid': 'Ingrese una fecha valida.'}, required=False
    )

    def clean_lugar(self):
        lugar = self.cleaned_data.get('lugar')
        if lugar == '':
            return None
        else:
            return lugar


    def clean_fecha_desde(self):
        fecha_desde = self.cleaned_data.get('fecha_desde')
        if fecha_desde is None:
            return fecha_desde
        else:
            hoy = datetime.now()
            if fecha_desde < hoy.date():
                raise forms.ValidationError('Debes ingresar una fecha de inicio mayor.')
        return fecha_desde

    def clean_fecha_hasta(self):
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        if fecha_hasta is None:
            return fecha_hasta
        else:
            fecha_desde = self.cleaned_data.get('fecha_desde')
            if fecha_desde is None:
                raise forms.ValidationError('Debes ingresar una fecha de inicio.')
            elif fecha_desde > fecha_hasta:
                raise forms.ValidationError('Rango de fechas inválido.')
            elif abs(fecha_hasta-fecha_desde).days > 60:
                raise forms.ValidationError('El rango entre las dos fecha puede ser, como máximo, de 2 meses.')
        return fecha_hasta