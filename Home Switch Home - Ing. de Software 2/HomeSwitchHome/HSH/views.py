from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth import views as auth_views
from HomeSwitchHome.forms import ResidenciaForm, PujaForm, HotsaleForm,BuscarResidenciasForm, RegistroForm, PerfilForm, EditarPerfilForm, \
    CambiarTarjetaForm, PrecioForm, CustomAuthForm, ContactoForm
from .models import Residencia, Subasta, Puja, Usuario, Perfil, Reserva, Precio, Hotsale
from .consultas import validar_ubicacion, obtener_subastas, generar_reservas, obtener_semanas, obtener_subastas_finalizadas, validar_ubicacion_editar, \
    validar_nombre_completo, obtener_reservas_para_hotsale
from datetime import datetime, timedelta


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
    if not request.user.is_staff:
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
    fecha_lunes = datetime(2019, 7, 15)
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
    context = {"subastas": info_return['subastas'], "subastas_finalizadas": obtener_subastas_finalizadas()}
    return render(request, template, context)


def pujar_page(request, subasta_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar tu sesion para acceder a esta funcion.')
        return redirect('/')
    if request.user.is_staff:
        return redirect('/')
    template = "pujar.html"
    form = PujaForm(request.POST or None)
    subasta = Subasta.objects.get(id=subasta_id)
    context = {"sub": subasta, "form": form}
    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data.get("monto") < subasta.obtener_monto_max():
                messages.error(request, 'Debe ingresar un monto mayor a la última puja.')
            else:
                if request.user.get_perfil().creditos == 0:
                    messages.error(request, 'No posee ningun credito para pujar.')
                else:
                    puja = Puja()
                    puja.monto = form.cleaned_data.get("monto")
                    puja.id_usuario = request.user.email
                    puja.id_subasta = subasta
                    puja.save()
                    messages.success(request, 'Su puja se ha registrado en la subasta.')
                    return HttpResponseRedirect(request.path_info)
    else:
        form = PujaForm(request.POST or None)
    return render(request, template, context)


def cerrar_subasta_page(request, subasta_id):
    if not request.user.is_staff:
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
        usuario_form = RegistroForm(request.POST or None)
        perfil_form = PerfilForm(request.POST or None)
        if usuario_form.is_valid() and perfil_form.is_valid():
            if not validar_nombre_completo(
                    perfil_form.cleaned_data.get('nombre'),
                    perfil_form.cleaned_data.get('apellido'),
                    perfil_form.cleaned_data.get('fecha_nacimiento')
            ):
                usuario = Usuario()
                usuario.fecha_registro = datetime.now()
                usuario.email = usuario_form.clean_email()
                usuario.set_password(usuario_form.clean_password2())
                usuario.save()
                perfil = Perfil(
                    nombre=perfil_form.cleaned_data.get('nombre'),
                    apellido=perfil_form.cleaned_data.get('apellido'),
                    fecha_nacimiento=perfil_form.clean_fecha_nacimiento(),
                    nro_tarjeta_credito=perfil_form.cleaned_data.get('nro_tarjeta_credito'),
                    marca_tarjeta_credito=perfil_form.cleaned_data.get('marca_tarjeta_credito'),
                    nombre_titular_tarjeta=perfil_form.cleaned_data.get('nombre_titular_tarjeta'),
                    fecha_vencimiento_tarjeta=perfil_form.clean_fecha_vencimiento_tarjeta(),
                    codigo_seguridad_tarjeta=perfil_form.cleaned_data.get('codigo_seguridad_tarjeta'),
                    mi_usuario=usuario,
                    vencimiento_creditos=(datetime.now() + timedelta(days=365.24))
                )
                perfil.save()
                raw_password = usuario_form.clean_password2()
                usuario = authenticate(email=usuario.email, password=raw_password)
                login(request, usuario)
                return redirect('/')
            else:
                messages.error(request, 'Ya existe una cuenta para este usuario.')
    else:
        usuario_form = RegistroForm()
        perfil_form = PerfilForm()
    return render(request, 'registro.html', {'usuario_form': usuario_form, 'perfil_form': perfil_form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthForm

    def form_valid(self, form):
        return super(CustomLoginView, self).form_valid(form)


def ver_usuarios_page(request):
    if not request.user.is_staff:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
    template = "listar_usuarios.html"
    return render(request, template, {"usuarios": Usuario.objects.filter(is_active=True, is_staff=False), "perfiles": Perfil.objects.filter()})


def registro_admin_page(request):
    if request.user.is_staff:
        form = RegistroForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                admin = Usuario()
                admin.fecha_registro = datetime.now()
                admin.email = form.clean_email()
                admin.set_password(form.clean_password2())
                admin.is_staff = True
                admin.save()
                messages.success(request, 'Se ha creado el nuevo administrador exitosamente.')
                return redirect('/')
        else:
            form = RegistroForm(request.POST or None)
    else:
        messages.error(request, 'Solo administradores pueden acceder a esta funcion.')
        return redirect('/')
    return render(request, 'registro_admin.html', {'form': form})


def perfil_page(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Inicia tu sesion para poder ver tu perfil.')
        return redirect('/iniciar_sesion/')
    template = 'perfil.html'
    usuario = Usuario.objects.get(email=request.user.email)
    perfil = usuario.get_perfil()
    reservas = usuario.get_reservas()
    nrotarjeta = '** - ********** - ' + (str(perfil.nro_tarjeta_credito)[-4:])
    return render(request, template, {
        'user': usuario,
        'perfil': perfil,
        'nrotarjeta': nrotarjeta,
        'precio':Precio.objects.get(),
        'reservas': reservas
    })


def editar_perfil_page(request, perfil):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar tu sesion para acceder a esta pagina.')
        return redirect('/')
    mi_perfil = Perfil.objects.get(id=perfil)
    if request.user.id != mi_perfil.mi_usuario.id:
        messages.error(request, '¡No puedes editar el perfil de otro usuario!')
        return redirect('/perfil/')
    template = 'editar_perfil.html'
    form = EditarPerfilForm(request.POST or None, initial={
        'nombre': mi_perfil.nombre,
        'apellido': mi_perfil.apellido,
        'fecha_nacimiento': mi_perfil.fecha_nacimiento.strftime("%d/%m/%Y"),
    })
    context = {'perfil': mi_perfil, 'form': form}
    if request.method == 'POST':
        if form.is_valid():
            if not validar_nombre_completo(
                    form.cleaned_data.get('nombre'),
                    form.cleaned_data.get('apellido'),
                    form.clean_fecha_nacimiento()
            ):
                form.editar(perfil)
                messages.success(request, 'Su perfil se ha editado exitosamente.')
                return redirect('/perfil/')
            else:
                messages.error(request, 'Ya existe un usuario similar cargado en el sistema.')
    else:
        form = EditarPerfilForm()
    return render(request, template, context)


def cambiar_tarjeta_page(request, perfil):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar tu sesion para acceder a esta pagina.')
        return redirect('/')
    mi_perfil = Perfil.objects.get(id=perfil)
    if request.user.id != mi_perfil.mi_usuario.id:
        messages.error(request, '¡No puedes editar el perfil de otro usuario!')
        return redirect('/perfil/')
    template = 'cambiar_tarjeta.html'
    form = CambiarTarjetaForm(request.POST or None, initial={
        'nro_tarjeta_credito': mi_perfil.nro_tarjeta_credito,
        'marca_tarjeta_credito': mi_perfil.marca_tarjeta_credito,
        'nombre_titular_tarjeta': mi_perfil.nombre_titular_tarjeta,
        'fecha_vencimiento_tarjeta': mi_perfil.fecha_vencimiento_tarjeta.strftime("%d/%m/%y"),
        'codigo_seguridad_tarjeta': mi_perfil.codigo_seguridad_tarjeta
    })
    context = {'perfil': mi_perfil, 'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.editar(perfil)
            messages.success(request, 'Su tarjeta se ha cambiado exitosamente.')
            return redirect('/perfil/')
    else:
        form = CambiarTarjetaForm()
    return render(request, template, context)


def config_precios_page(request):
    if request.user.is_staff:
        template = "configprecios.html"
        precio = Precio.objects.get()
        form = PrecioForm(request.POST or None, initial={
            'precio_Normal': precio.precio_Normal,
            'precio_Premium': precio.precio_Premium
        })
        context = {"form": form, "precio": precio}
        if request.method == 'POST':
            if form.is_valid():
                precio.editar_precio(form.clean_precio_Normal(), form.clean_precio_Premium())
                messages.success(request, 'Los precios han sido actualizados exitosamente.')
                return redirect("/")
    return render(request, template, context)


def pasar_a_page(request, tipo, usuario):
    if not request.user.is_staff:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
    usu = Usuario.objects.get(id=usuario)
    template = "pasar_a_page.html"
    context = {"usu": usu}
    if request.method == 'POST':
        if tipo == "1":
            usu.is_active = False
            usu.save()
            messages.success(request, 'El administrador ha sido eliminado.')
            return redirect("http://127.0.0.1:8000/ver_administradores/")
        elif tipo == "2":
            usu.is_premium = False
        else:
            usu.is_premium = True
        usu.save()
        messages.success(request, 'El cambio ha sido registrado.')
        return redirect("http://127.0.0.1:8000/ver_usuarios/")
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)


def ver_residencia_page(request, residencia):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar tu sesion para acceder a esta pagina.')
        return redirect('/')
    template = "ver_residencia.html"
    activas = obtener_subastas(datetime(2019, 7, 15))
    res=Residencia.objects.get(id=residencia)
    reservas=Reserva.objects.filter(id_residencia=res)
    inactivas=Subasta.objects.filter(
        ~Q(fecha_inicio=datetime(2019, 7, 15)),
        Q(esta_programada=True),
    )
    subastas=[]
    for rese in reservas:
        subastas.append(Subasta.objects.get(id_reserva=rese))
    context = {"res": res, "subastas": subastas, "activas": activas, "inactivas": inactivas}
    if request.method == 'POST':
        messages.success(request, 'La residencia se ha editado exitosamente.')
        return redirect("/")
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)


def reservar_residencia_page(request, reserva):
    if not request.user.is_authenticated:
        if not request.user.is_premium:
            messages.error(request, 'Debes ser un usuario premium para acceder a esta funcion.')
            return redirect('/')
    template = "reservar_residencia.html"
    if request.method == 'POST':
        if request.user.get_perfil().creditos>0:
            res=Reserva.objects.get(id=reserva)
            res.reservar(request.user.email)
            messages.success(request, 'La reserva ha sido realizada exitosamente.')
            return redirect("/")
        else:
            messages.error(request, 'No posee creditos suficientes para realizar esta reserva.')
            return redirect("http://127.0.0.1:8000/ver_residencias")
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template)


def buscar_residencia(request):
    form = BuscarResidenciasForm(request.POST or None)
    template = "buscar_residencia.html"
    context = {"form": form}
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                lugar = form.clean_lugar()
                fecha_desde = form.clean_fecha_desde()
                fecha_hasta = form.clean_fecha_hasta()
                semanas = obtener_semanas(lugar, fecha_desde, fecha_hasta)
                en_subasta = (helper_listar_subastas())['subastas']
                actuales=[]
                for en_sub in en_subasta:
                    for sem in semanas:
                        if en_sub.id_reserva == sem:
                            semanas.remove(sem)
                            actuales.append(sem)
                context2 = {"semanas": semanas, "actuales": actuales}
                return render(request, 'mostrar_resultados.html', context2)
    else:
        messages.error(request, 'Debes iniciar tu sesion para acceder a esta pagina.')
    return render(request, template, context)


def ayuda_page(request):
    return render(request, "ayuda.html")


def ver_admins_page(request):
    if not request.user.is_staff:
        messages.error(request, 'Solo los administradores pueden acceder a esta funcion.')
        return redirect('/')
    template = "listar_admins.html"
    return render(request, template, {"usuarios": Usuario.objects.filter(is_active=True, is_staff=True)})


def ver_reservas_para_hotsale(request):
    if request.user.is_staff:
        template = 'ver_reservas_para_hotsale.html'
        context = {'reservas': obtener_reservas_para_hotsale()}
        return render(request, template, context)

    else:
        return redirect('/')


def configurar_hotsale_page(request, reserva):
    if request.user.is_staff:
        template = "configurar_hotsale.html"
        form = HotsaleForm(request.POST or None)
        res = Reserva.objects.get(id=reserva)
        context = {'form': form }
        if request.method == 'POST':
            if form.is_valid():
                precio = form.clean_precio()
                hotsale = Hotsale()
                hotsale.id_reserva = res
                hotsale.precio = precio
                hotsale.save()
                messages.success(request, 'El hotsale se ha creado exitosamente.')
                return redirect('http://127.0.0.1:8000/')
        else:
            form = ResidenciaForm(request.POST or None)
        return render(request, template, context)
    else:
        return redirect('/')


def listar_hotsales_page(request):
    if not request.user.is_authenticated:
        return redirect('/')
    template = "listar_hotsales.html"
    hotsales = Hotsale.objects.filter(esta_programado=False)
    context = {"hotsales": Hotsale.objects.filter(esta_programado=True), 'hotsales_finalizados': hotsales}
    return render(request, template, context)


def ver_hotsale_page(request, hotsale):
    if not request.user.is_authenticated:
        return redirect('/')
    template = "ver_hotsale.html"
    hotsale = Hotsale.objects.get(id=hotsale)
    context = {"hotsale": hotsale}
    if request.method == 'POST':
        hotsale.esta_programado=False
        hotsale.id_reserva.usuario_ganador=request.user.email
        hotsale.id_reserva.save()
        hotsale.save()
        messages.success(request, 'El hotsale se ha adquirido exitosamente.')
        return redirect('http://127.0.0.1:8000/')
    else:
        form = ResidenciaForm(request.POST or None)
    return render(request, template, context)

def cerrar_hotsale_page(request, hotsale):
    if request.user.is_staff:
        hotsale = Hotsale.objects.get(id=hotsale)
        template = 'cerrar_hotsale.html'
        context = {"hotsale": hotsale}
        if request.method == 'POST':
            hotsale.esta_programado = False
            hotsale.save()
            messages.success(request, 'El hotsale se ha cancelado exitosamente.')
            return redirect('http://127.0.0.1:8000/')
    else:
        return redirect('/')
    return render(request, template, context)

def contacto_page(request):
    if request.user.is_staff:
        return redirect('/')
    if request.user.is_authenticated:
        form = ContactoForm(request.POST or None, initial={'email':request.user.email})
    else:
        form = ContactoForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            messages.success(request, "Su mensaje ha sido enviado. Tendra su respuesta dentro de los proximos 7 dias laborables.")
            return redirect('/')
    return render(request, "contactenos.html", {'form': form})