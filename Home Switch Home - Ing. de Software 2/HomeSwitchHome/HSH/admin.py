from django.contrib import admin
from .models import Residencia, Subasta, Puja, Reserva, Usuario, Precio

# Register your models here.

admin.site.register(Residencia)
admin.site.register(Subasta)
admin.site.register(Puja)
admin.site.register(Reserva)
admin.site.register(Usuario)
admin.site.register(Precio)