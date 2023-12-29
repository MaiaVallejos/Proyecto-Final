from django.contrib import admin
from .models import Contacto

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
   list_display = ('id', 'nombre_apellido', 'email', 'asunto', 'fecha')