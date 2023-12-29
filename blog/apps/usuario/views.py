from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Usuario
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.models import Group

# Create your views here.

class RegistrarUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm
   
    def form_valid(self, form):
       messages.success(self.request, 'Registro exitoso. Por favor, inicia sesión.')
       form.save()

       return redirect('apps.usuario:registrar')

class LoginUsuario(LoginView):
    template_name = 'registration/login.html'
  
    def get_success_url(self):
        messages.success(self.request, 'Login exitoso')

        return reverse('apps.usuario:login')

class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'
    next_page = reverse_lazy('apps.posts:posts')

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Logout exitoso')
        return super().dispatch(request, *args, **kwargs)
        
    

class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuario/eliminar_usuario.html'
    success_url = reverse_lazy('apps.usuario:usuario_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name='Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_colaborador
        return context

    def post(self, request, *args, **kwargs):
        eliminar_comentarios = request.POST.get('eliminar_comentarios', False)
        eliminar_posts = request.POST.get('eliminar_posts', False)
        self.object = self.get_object()
        if eliminar_comentarios:
           Comentario.objects.filter(usuario=self.object).delete()

        if eliminar_posts:
          Post.objects.filter(autor=self.object).delete()
        messages.success(request, f'Usuario {self.object.username} eliminado correctamente')
        return self.delete(request, *args, **kwargs)
