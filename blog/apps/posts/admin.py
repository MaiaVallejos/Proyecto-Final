from django.contrib import admin
from .models import Categoria, Post, Comentario

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
        list_display = ('id', 'titulo', 'subtitulo', 'fecha', 'texto',
                     'activo', 'categoria', 'imagen', 'publicado')
admin.site.register(Categoria)
admin.site.register(Comentario)