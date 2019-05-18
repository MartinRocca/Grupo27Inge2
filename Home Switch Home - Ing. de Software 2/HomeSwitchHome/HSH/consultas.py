from .models import Residencia
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


def validar_ubicacion(una_localidad, una_calle, un_numero):
    # Si ya existe una residencia con la localidad, direccion y nombre
    # pasados por parámetro, la funcion devuelve true. Caso contrario false.
    try:
        Residencia.objects.get(
            Q(localidad__iexact=una_localidad),
            Q(calle__iexact=una_calle),
            Q(nro_direccion=un_numero)
        )
        return True
    except ObjectDoesNotExist:
        return False
