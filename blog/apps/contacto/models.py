from django.db import models
from django.utils import timezone


class Contacto(models.Model):
    nombre_apellido = models.CharField(max_length=120)
    email = models.EmailField()
    asunto = models.CharField(max_length=50)
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

def _str_(self):
   return self.nombre_apellido
