from django.shortcuts import render, redirect
from django.contrib import messages
from HomeSwitchHome.forms import ResidenciaForm
from .models import Residencia
from .consultas import validar_ubicacion


# Create your views here.

def home_page(request):
    return render(request, "home_page.html", {'titulo':"Bienvenido a HSH"})


def crear_residencia_page(request):
    template = "crear_residencia.html"
    form = ResidenciaForm(request.POST or None)
    context = {"form": form, "titulo": "Cargar residencia"}
    # HTTP Method POST. That means the form was submitted by a user
    # and we can find her filled out answers using the request.
    if request.method == 'POST':
        # A Form instance has an is_valid() method, which runs validation routines for all its fields.
        # if all fields contain valid data, it will return True and place the form’s data in its cleaned_data attribute.
        if form.is_valid():
            if not validar_ubicacion(form.cleaned_data['localidad'], form.cleaned_data['calle'],
                                      form.cleaned_data['nro_direccion']):
                form.save()
                messages.success(request, 'La residencia se ha cargado exitosamente en el sistema.')
                form = ResidenciaForm(request.POST or None)
                return redirect("http://127.0.0.1:8000/crear_residencia")
            else:
                messages.error(request, 'Ya existe una residencia similar cargada en el sistema.')
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)


def listar_residencias_page(request):
    template = "listar_residencias.html"
    return render(request, template, {"residencias": Residencia.objects.all})

def editar_residencia_page(request, residencia):
    template = "editar_residencia.html"
    form = ResidenciaForm(request.POST or None)
    context = {"res": Residencia.objects.get(id=residencia), "form": form}
    if request.method == 'POST':
        if form.is_valid():
            if not validar_ubicacion(form.cleaned_data['localidad'], form.cleaned_data['calle'],
                                      form.cleaned_data['nro_direccion']):
                form.save(residencia)
                form = ResidenciaForm(request.POST or None)
                return redirect("/")
            else:
                messages.error(request, 'Ya existe una residencia similar cargada en el sistema.')
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)
