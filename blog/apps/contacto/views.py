from .forms import ContactoForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy


class ContactoUsuario(CreateView):
  template_name = 'contacto/contacto.html'
  form_class = ContactoForm
  success_url = reverse_lazy('apps.contacto:contacto')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['request'] = self.request
    return context

  def form_valid(self, form):
    messages.success(self.request, 'Consulta enviada.') 
    return super().form_valid(form)