from django.shortcuts import render
from HomeSwitchHome.forms import ResidenciaForm
from .models import Residencia
from .consultas import validar_existencia


# Create your views here.

def home_page(request):
    return render(request, "home_page.html", {"titulo": "Bienvenido a Home Switch Home"})


def crear_residencia_page(request):
    form = ResidenciaForm(request.POST or None)
    template = "crear_residencia.html"
    context = {"form": form, "titulo": "Cargar residencia"}
    # ----
    # HTTP Method POST. That means the form was submitted by a user
    # and we can find her filled out answers using the request.
    if request.method == 'POST':
        # A Form instance has an is_valid() method, which runs validation routines for all its fields.
        # if all fields contain valid data, it will return True and place the form’s data in its cleaned_data attribute.
        if form.is_valid():
            if not validar_existencia(form.cleaned_data['localidad'], form.cleaned_data['calle'],
                                      form.cleaned_data['nro_direccion']):
                r = Residencia()
                r.localidad = form.cleaned_data['localidad']
                r.nombre = form.cleaned_data['nombre']
                r.descripcion = form.cleaned_data['descripcion']
                r.precio_base = form.cleaned_data['precio_base']
                r.limite_personas = form.cleaned_data['limite_personas']
                r.nro_direccion = form.cleaned_data['nro_direccion']
                r.calle = form.cleaned_data['calle']
                r.cant_habitaciones = form.cleaned_data['cant_habitaciones']
                r.save()
            else:
                print('Ya existe una residencia similar cargada en el sistema.')
            # form = ResidenciaForm()
    return render(request, template, context)
