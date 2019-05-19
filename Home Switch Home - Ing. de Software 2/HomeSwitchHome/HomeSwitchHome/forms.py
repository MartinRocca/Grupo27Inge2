from django import forms
from HSH.models import Residencia, Puja, Subasta

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
    email = forms.EmailField()
    monto = forms.FloatField()
    subasta = forms.CharField(widget=forms.HiddenInput())

    def clean_monto(self):
        sub = Subasta.objects.get(id=self.cleaned_data.get('subasta'))
        if sub.obtener_monto_max() > self.cleaned_data['monto']:
            raise forms.ValidationError("El monto a pujar debe superar el valor de la última puja")
        return self.cleaned_data['monto']

    def save(self):
        p = Puja()
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        p.id_usuario = self.cleaned_data['email']
        #sub = Subasta.objects.get(id=subasta)
        print("self.cleaned_data['subasta']")
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        #if sub.obtener_monto_max() > self.cleaned_data['monto']:
        #    raise forms.ValidationError("El monto a pujar debe superar el valor de la última puja")
        #p.monto = self.cleaned_data['monto']
        p.monto = self.clean_monto()
        p.id_subasta = Subasta.objects.get(id=subasta)
        p.save()


















class UsuarioForm(forms.Form):
    email = forms.EmailField()
    contraseña = forms.CharField()
    tarjeta_credito = forms.CharField()
    creditos = forms.IntegerField()
    fecha_nac = forms.DateField()
    nombre = forms.CharField()

    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')