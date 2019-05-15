from django import forms
from HSH.models import Residencia

class ResidenciaForm(forms.Form):
    localidad = forms.CharField()
    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    precio_base = forms.FloatField()
    limite_personas = forms.IntegerField()
    nro_direccion = forms.IntegerField()
    calle = forms.CharField()
    cant_habitaciones = forms.IntegerField()
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