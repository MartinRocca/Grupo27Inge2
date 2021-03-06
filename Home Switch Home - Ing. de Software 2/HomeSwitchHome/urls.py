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
from HSH.views import (
    home_page,
    crear_residencia_page,
    listar_residencias_page,
    editar_residencia_page,
    eliminar_residencia_page,
    listar_subastas_page,
    pujar_page,
    cerrar_subasta_page,
    listar_subastas_finalizadas_page,
    registro_page,
)

urlpatterns = [
    path('admin', admin.site.urls),
    path('', home_page),
    path('crear_residencia', crear_residencia_page),
    path('ver_residencias', listar_residencias_page),
    path('tinymce/', include('tinymce.urls')),
    path('editar_residencia/<residencia>/', editar_residencia_page, name='editar_residencia'),
    path('eliminar_residencia/<residencia>/', eliminar_residencia_page, name='eliminar_residencia'),
    path('ver_subastas', listar_subastas_page),
    path('pujar/<int:subasta_id>/', pujar_page, name='pujar'),
    path('cerrar_subasta/<int:subasta_id>/', cerrar_subasta_page, name='cerrar_subasta'),
    path('ver_subastas_finalizadas', listar_subastas_finalizadas_page),
    path('registrarse/', registro_page, name = 'registrarse')
]
