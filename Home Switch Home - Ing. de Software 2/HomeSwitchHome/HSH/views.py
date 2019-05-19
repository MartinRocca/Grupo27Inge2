from django.shortcuts import render, redirect
from django.contrib import messages
from HomeSwitchHome.forms import ResidenciaForm, PujaForm
from .models import Residencia, Subasta
from .consultas import validar_ubicacion, obtener_subastas, generar_reservas
import datetime

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
                residencia_cargada = form.save()
                messages.success(request, 'La residencia se ha cargado exitosamente en el sistema.')
                generar_reservas(residencia_cargada)
                form = ResidenciaForm(request.POST or None)
                return redirect("http://127.0.0.1:8000/crear_residencia")
            else:
                messages.error(request, 'Ya existe una residencia similar cargada en el sistema.')
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)


def listar_residencias_page(request):
    template = "listar_residencias.html"
    return render(request, template, {"residencias": Residencia.objects.filter(activa=True)})

def editar_residencia_page(request, residencia):
    template = "editar_residencia.html"
    form = ResidenciaForm(request.POST or None)
    context = {"res": Residencia.objects.get(id=residencia), "form": form}
    if request.method == 'POST':
        if form.is_valid():
            if not validar_ubicacion(form.cleaned_data['localidad'], form.cleaned_data['calle'],
                                      form.cleaned_data['nro_direccion']):
                form.editar(residencia)
                form = ResidenciaForm(request.POST or None)
                return redirect("/")
            else:
                messages.error(request, 'Ya existe una residencia similar cargada en el sistema.')
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)

def eliminar_residencia_page(request, residencia):
    template = "eliminar_residencia.html"
    context = {"res": Residencia.objects.get(id=residencia)}
    if request.method == 'POST':
        (context["res"]).borrar()
        return redirect("/")
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)

def helper_listar_subastas():
    # fecha = datetime.now()
    # Creo una variable date donde el día sea lunes y si o si encuentre subastas.
    fecha_lunes = datetime.datetime(2019, 5, 20)
    info_return = {}
    subastas_activas = []
    # if fecha.weekday() in [1, 2, 3]:
    #    if fecha.weekday() == 1:
    #        subastas_activas = obtener_subastas(fecha)
    #    else:
    #        if fecha.weekday() == 2:
    #            subastas_activas = obtener_subastas(fecha - timedelta(days=1))
    #        else:
    #            subastas_activas = obtener_subastas(fecha - timedelta(days=2))
    #    if not subastas_activas:
    #        info_return['codigo_error'] = 1
    # else:
    #    info_return['codigo_error'] = 2
    subastas_activas = obtener_subastas(fecha_lunes)
    info_return['subastas'] = subastas_activas
    info_return['codigo_error'] = 0
    return info_return


def listar_subastas_page(request):
    template = "listar_subastas.html"
    info_return = helper_listar_subastas()
    if info_return['codigo_error'] == 1:
        messages.error(request, 'No hay subastas disponibles.')
    elif info_return['codigo_error'] == 2:
        messages.error(request, 'Hoy no es día de subastas. Por favor, vuelva el próximo lunes.')
    context = {"subastas": info_return['subastas']}
    return render(request, template, context)

def pujar_page(request, subasta):
    template = "pujar.html"
    form = PujaForm(request.POST or None, initial={'subasta': subasta})
    context = {"sub": Subasta.objects.get(id=subasta), "form": form}
    print(type(subasta))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = PujaForm(request.POST or None)
    return render(request, template, context)