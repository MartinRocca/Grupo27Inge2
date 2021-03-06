"""HomeSwitchHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from HSH.views import (
    home_page,
    crear_residencia_page,
    listar_residencias_page,
    editar_residencia_page,
    eliminar_residencia_page,
    listar_subastas_page,
    pujar_page,
    cerrar_subasta_page,
    ver_usuarios_page,
    registro_page,
    registro_admin_page,
    perfil_page,
    editar_perfil_page,
    cambiar_tarjeta_page,
    config_precios_page,
    pasar_a_page,
    reservar_residencia_page,
    ver_residencia_page,
    CustomLoginView,
    buscar_residencia,
    ayuda_page,
    ver_admins_page,
    ver_reservas_para_hotsale,
    configurar_hotsale_page,
    listar_hotsales_page,
    ver_hotsale_page,
    cerrar_hotsale_page,
    contacto_page,
)

urlpatterns = [
    path('admin', admin.site.urls),
    path('', home_page),
    path('crear_residencia', crear_residencia_page),
    path('ver_residencias', listar_residencias_page),
    path('tinymce/', include('tinymce.urls')),
    path('editar_residencia/<residencia>/', editar_residencia_page, name='editar_residencia'),
    path('eliminar_residencia/<residencia>/', eliminar_residencia_page, name='eliminar_residencia'),
    path('ver_residencia/<residencia>/', ver_residencia_page, name='ver_residencia'),
    path('reservar_residencia/<reserva>/', reservar_residencia_page, name='reservar_residencia'),
    path('ver_subastas/', listar_subastas_page),
    path('pujar/<int:subasta_id>/', pujar_page, name='pujar'),
    path('cerrar_subasta/<int:subasta_id>/', cerrar_subasta_page, name='cerrar_subasta'),
    path('ver_usuarios/', ver_usuarios_page),
    path('iniciar_sesion/', CustomLoginView.as_view(template_name='login.html')),
    path('cerrar_sesion/', auth_views.LogoutView.as_view(template_name='logout.html')),
    path('registrarse/', registro_page),
    path('registrar_admin/', registro_admin_page),
    path('perfil/', perfil_page),
    path('editar_perfil/<perfil>/', editar_perfil_page, name='editar_perfil'),
    path('cambiar_tarjeta/<perfil>/', cambiar_tarjeta_page, name='cambiar_tarjeta'),
    path('config_precios/', config_precios_page),
    path('pasar_a/<tipo>/<usuario>/', pasar_a_page, name='pasar_a'),
    path('buscar_residencia/', buscar_residencia),
    path('ayuda/', ayuda_page),
    path('ver_administradores/', ver_admins_page),
    path('ver_reservas_para_hotsale/', ver_reservas_para_hotsale),
    path('crear_hotsale/<reserva>/', configurar_hotsale_page, name='configurar_hotsale'),
    path('listar_hotsales/', listar_hotsales_page),
    path('ver_hotsale/<hotsale>/', ver_hotsale_page, name='ver_hotsale'),
    path('cerrar_hotsale/<hotsale>/', cerrar_hotsale_page, name='cerrar_hotsale'),
    path('contactenos/', contacto_page)
]
