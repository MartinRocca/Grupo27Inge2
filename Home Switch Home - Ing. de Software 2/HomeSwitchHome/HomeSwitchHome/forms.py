from django import forms

class ResidenciaForm(forms.Form):
    localidad = forms.CharField()
    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    precio_base = forms.FloatField()
    limite_personas = forms.IntegerField()
    nro_direccion = forms.IntegerField()
    calle = forms.CharField()
    cant_habitaciones = forms.IntegerField()