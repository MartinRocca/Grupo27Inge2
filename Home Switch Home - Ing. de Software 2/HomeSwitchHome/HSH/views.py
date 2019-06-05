from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from HomeSwitchHome.forms import ResidenciaForm, PujaForm, RegistroForm, PerfilForm
from .models import Residencia, Subasta, Puja, Usuario, Perfil
from .consultas import validar_ubicacion, obtener_subastas, generar_reservas, validar_ubicacion_editar
import datetime


# Create your views here.

def home_page(request):
    return render(request, "home_page.html", {'titulo': "Bienvenido a HSH", 'user': request.user})

def crear_residencia_page(request):
    if request.user.is_staff == False:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
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
                return redirect('/')
            else:
                messages.error(request, 'Ya existe una residencia similar cargada en el sistema.')
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)

def listar_residencias_page(request):
    template = "listar_residencias.html"
    return render(request, template, {"residencias": Residencia.objects.filter(activa=True)})

def editar_residencia_page(request, residencia):
    if request.user.is_staff == False:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
    template = "editar_residencia.html"
    datos = model_to_dict(Residencia.objects.filter(id=residencia)[0])
    # Residencia.object.filter y .get me devuelven un dato de tipo QuerySet; este funciona similar a una lista de python
    # regular, excepto que sus contenidos seran las tuplas que me devolvio la base de datos. filter(id=residencia) me
    # devuelve solo una tupla (la que se quiere editar), la cual puedo usar para crear un diccionario con sus datos.

    # Luego, puedo pasarle este diccionario al formulario cuando esta siendo creado, con el argumento 'initial= ', para
    # que los valores que le paso en ese diccionario sean los predeterminados del formulario (Y asi aparescan escritos
    # de entrada.
    form = ResidenciaForm(request.POST or None, initial=datos)
    context = {"res": Residencia.objects.get(id=residencia), "form": form}
    if request.method == 'POST':
        if form.is_valid():
            if not validar_ubicacion_editar(form.cleaned_data['localidad'], form.cleaned_data['calle'],
                                     form.cleaned_data['nro_direccion'], Residencia.objects.get(id=residencia)):
                form.editar(residencia)
                form = ResidenciaForm(request.POST or None)
                print("Entra acá")
                messages.success(request, 'La residencia se ha editado exitosamente.')
                return redirect("/")
            else:
                messages.error(request, 'Ya existe una residencia similar cargada en el sistema.')
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)

def eliminar_residencia_page(request, residencia):
    if request.user.is_staff == False:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
    template = "eliminar_residencia.html"
    residencia = Residencia.objects.get(id=residencia)
    context = {"res": residencia}
    if request.method == 'POST':
        residencia.borrar()
        messages.success(request, 'La residencia se ha borrado exitosamente.')
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

def listar_subastas_finalizadas_page(request):
    if request.user.is_staff == False:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
    template = "listar_subastas_finalizadas.html"
    subastas = Subasta.objects.filter(esta_programada=False)
    context = {"subastas": subastas}
    return render(request, template, context)

def pujar_page(request, subasta_id):
    template = "pujar.html"
    form = PujaForm(request.POST or None)
    subasta = Subasta.objects.get(id=subasta_id)
    context = {"sub": subasta, "form": form}
    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data.get("monto") < subasta.obtener_monto_max():
                messages.error(request, 'Debe ingresar un monto mayor a la última puja.')
            else:
                puja = Puja()
                puja.monto = form.cleaned_data.get("monto")
                puja.id_usuario = form.cleaned_data.get("email")
                puja.id_subasta = subasta
                puja.save()
                messages.success(request, 'Su puja se ha registrado en la subasta.')
                return HttpResponseRedirect(request.path_info)
    else:
        form = PujaForm(request.POST or None)
    return render(request, template, context)

def cerrar_subasta_page(request, subasta_id):
    if request.user.is_staff == False:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
    template = "cerrar_subasta.html"
    subasta = Subasta.objects.get(id=subasta_id)
    context = {"sub": subasta}
    if request.method == 'POST':
        subasta.cerrar_subasta()
        messages.success(request, 'La subasta se ha cerrado exitosamente')
        return redirect("/")
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)

def registro_page(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Ya tienes una sesion activa.')
        return redirect('/')
    if request.method == 'POST':
        usuario_form = RegistroForm(request.POST)
        perfil_form = PerfilForm(request.POST)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario = Usuario()
            usuario.email = usuario_form.clean_email()
            usuario.set_password(usuario_form.clean_password2())
            usuario.save()
            perfil = Perfil(
                nombre = perfil_form.cleaned_data.get('nombre'),
                apellido = perfil_form.cleaned_data.get('apellido'),
                fecha_nacimiento = perfil_form.clean_fecha_nacimiento(),
                nro_tarjeta_credito = perfil_form.cleaned_data.get('nro_tarjeta_credito'),
                marca_tarjeta_credito = perfil_form.cleaned_data.get('marca_tarjeta_credito'),
                nombre_titular_tarjeta = perfil_form.cleaned_data.get('nombre_titular_tarjeta'),
                fecha_vencimiento_tarjeta = perfil_form.clean_fecha_vencimiento_tarjeta(),
                codigo_seguridad_tarjeta = perfil_form.cleaned_data.get('codigo_seguridad_tarjeta'),
                mi_usuario = usuario,
            )
            perfil.save()
            raw_password = usuario_form.clean_password2()
            usuario = authenticate(email = usuario.email, password = raw_password)
            login(request, usuario)
            return redirect('/')
    else:
        usuario_form = RegistroForm(request.POST)
        perfil_form = PerfilForm(request.POST)
    return render(request, 'registro.html', {'usuario_form': usuario_form, 'perfil_form': perfil_form})

def ver_usuarios_page(request):
    if request.user.is_staff == False:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
    template = "listar_usuarios.html"
    return render(request, template, {"usuarios": Usuario.objects.all()})

def registro_admin_page(request):
    if request.user.is_staff:
        form = RegistroForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                 admin = Usuario()
                 admin.email = form.clean_email()
                 admin.set_password(form.clean_password2())
                 admin.is_staff = True
                 admin.save()
                 messages.success(request, 'Se ha creado el nuevo administrador exitosamente. Cierre esta sesion para iniciar sesion con el nuevo administrador.')
        else:
            form = RegistroForm(request.POST or None)
    else:
        messages.error(request, 'Solo administradores pueden acceder a esta funcion.')
        return redirect('/')
    return render(request, 'registro_admin.html', {'form': form})