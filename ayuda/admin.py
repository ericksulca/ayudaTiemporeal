from django.contrib import admin


# Register your models here.
from .models import *

admin.site.register(Persona)
admin.site.register(Item)
admin.site.register(Requisito)
admin.site.register(Tipooperacion)
admin.site.register(Operacion)
