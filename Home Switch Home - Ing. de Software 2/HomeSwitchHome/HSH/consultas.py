from .models import Residencia, Reserva, Subasta, Puja, Perfil
from django.db.models import Q, Max
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta


def validar_ubicacion(una_localidad, una_calle, un_numero):
    # Si ya existe una residencia con la localidad, direccion y nombre
    # pasados por parámetro, la funcion devuelve true. Caso contrario false.
    try:
        Residencia.objects.get(
            Q(localidad__iexact=una_localidad),
            Q(calle__iexact=una_calle),
            Q(nro_direccion=un_numero),
            Q(activa=True),
        )
        return True
    except ObjectDoesNotExist:
        return False

def validar_ubicacion_editar(una_localidad, una_calle, un_numero, una_residencia):
    # Si ya existe una residencia con la localidad, direccion y nombre
    # pasados por parámetro, la funcion devuelve true. Caso contrario false.
    try:
        res = Residencia.objects.get(
            Q(localidad__iexact=una_localidad),
            Q(calle__iexact=una_calle),
            Q(nro_direccion=un_numero),
            Q(activa=True),
        )
        if res == una_residencia:
            return False
        else:
            return True
    except ObjectDoesNotExist:
        return False

def generar_reservas(una_residencia):
    fecha_reserva = datetime.now() + timedelta(weeks=26)
    # Creo una fecha a los 6 meses de la fecha actual. 6 meses son aproximandamente 26 semanas.
    # Esta fecha se va a usar para generar la primer reserva en el plazo de los 6 meses
    # Por lo tanto ya ea posible realizar la subasta al lunes próximo de la fecha actual.

    # Suponemos que las semanas para ir a alojarte a una residencia comienzan los lunes (weekday = 0).
    # weekday():  Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
    # Seteo a la fecha creada para la reserva que sea un lunes.
    while fecha_reserva.weekday() != 0:
        fecha_reserva = fecha_reserva + timedelta(days=1)

    fecha_subasta = datetime.now()
    while fecha_subasta.weekday() != 0:
        fecha_subasta = fecha_subasta + timedelta(days=1)

    # Creación de 10 reservas y sus respectivas subastas.
    for i in range(10):
        reserva = Reserva()
        reserva.fecha = fecha_reserva
        reserva.id_residencia = una_residencia
        reserva.save()
        subasta = Subasta()
        subasta.id_reserva = reserva
        subasta.fecha_inicio = fecha_subasta
        subasta.save()
        fecha_reserva = fecha_reserva + timedelta(weeks=1)
        fecha_subasta = fecha_subasta + timedelta(weeks=1)

def obtener_subastas(fecha):
    try:
        subastas_activas = Subasta.objects.filter(
            Q(fecha_inicio=fecha),
            Q(esta_programada=True),
        )
        return subastas_activas
    except ObjectDoesNotExist:
        return []

def validar_nombre_completo(un_nombre, un_apellido, una_fecha):
    # Si ya existe un perfil con el mismo nombre, apellido y fecha de nacimiento que me pasan como parametro,
    # Devuelve true, caso contrario false
    try:
        per = Perfil.objects.get(
            Q(nombre__iexact=un_nombre),
            Q(apellido__iexact=un_apellido),
            Q(fecha_nacimiento=una_fecha)
        )
        return True
    except ObjectDoesNotExist:
        return False