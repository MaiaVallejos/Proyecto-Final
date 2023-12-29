
from .models import Comentario, Post, Categoria
from .forms import ComentarioForm, CrearPostForm, NuevaCategoriaForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy



class PostListView(ListView):
    model = Post
    template_name = "post/posts.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = super().get_queryset()
        orden = self.request.GET.get('orden')
        if orden == 'reciente':
            queryset = queryset.order_by('-fecha')
        elif orden == 'antiguo':
            queryset = queryset.order_by('fecha')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "post/post_individual.html"
    context_object_name = "post"
    pk_url_kwarg = "id"
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(posts_id=self.kwargs['id'])
        return context

    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.posts_id = self.kwargs['id']
            comentario.save()
            return redirect('apps.posts:post_individual', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

class PostCreateView(CreateView):
    model = Post
    form_class = CrearPostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')

class PostUpdateView(UpdateView):
    model = Post
    form_class = CrearPostForm
    template_name = "post/modificar_post.html"
    success_url = reverse_lazy('apps.posts:posts')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/eliminar_post.html'
    success_url = reverse_lazy('apps.posts:posts') 


class PostsPorCategoriaView(DetailView):
    model = Post
    template_name = 'posts/posts_por_categoria.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(categoria_id=self.kwargs['pk'])


class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    template_name = 'posts/crear_categoria.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
           return next_url
        else:
          return reverse_lazy('apps.posts:post_create') 

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'post/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'post/categoria_confirm_delete.html'
    success_url = reverse_lazy('apps.posts:categoria_list')

class ComentarioCreateView(CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/agregarComentario.html'
    success_url = 'comentario/comentarios/'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.posts_id = self.kwargs['posts_id']
        return super().form_valid(form)

class ComentarioUpdateView(UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/comentario_form.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
           return next_url
        else:
           return reverse('apps.posts:post_individual', args= [self.object.posts.id])

class ComentarioDeleteView(DeleteView):
    model = Comentario
    template_name = 'comentario/comentario_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('apps.posts:post_individual', args= [self.object.posts.id])