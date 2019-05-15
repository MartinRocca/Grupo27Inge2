from .models import Residencia
from django.core.exceptions import ObjectDoesNotExist

def validar_existencia(unaLocalidad):
    # Si ya existe una residencia con la localidad pasada por parámetro, la funcion devuelve true. Caso contrario false.
    try:
        aux = Residencia.objects.get(localidad=unaLocalidad)
        return True
    except ObjectDoesNotExist:
        return False