
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView,)
from core.models import *
from django.shortcuts import render
from .urls import *
from .forms import *

# Funciones encargadas para el renderizado de paginas

def dashboard_home(request):
    return render(request, "pages/home.html")

def dashboard_clientes(request):
    return render(request, "pages/clientes.html")

def dashboard_ventas(request):
    return render(request, "pages/ventas.html")

def dashboard_estadisticas(request):
    return render(request, "pages/estadisticas.html")

def dashboard_reportes(request):
    return render(request, "pages/reportes.html")

def dashboard_perfil(request):
    return render(request, "pages/perfil.html")


# Vista basa en clases para listar todos los lotes
class LoteListView(LoginRequiredMixin, ListView):
    model = Lote
    template_name = "pages/home.html"
    context_object_name = "lotes"
    def get_queryset(self):
        # Filtra los lotes para mostrar solo los que pertenecen al usuario actual.
        # `self.request.user` es el usuario que ha iniciado sesión.
        return Lote.objects.filter(id_usuario_propietario=self.request.user)

# Vista para crear un nuevo lote
class LoteCreateView(LoginRequiredMixin, CreateView):
    model = Lote
    template_name = "components/formularios/lotes/lote_form.html"
    form_class = LoteForm
    success_url = reverse_lazy("dashboard:dashboard_home")

    # Sobreescribe el método form_valid para asignar el usuario actual al lote
    def form_valid(self, form):
        Usuario = get_user_model()
        # Asigna el usuario actual como propietario del lote
        form.instance.id_usuario_propietario = self.request.user
        return super().form_valid(form)


# Vista para actualizar un lote existente
class LoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Lote
    template_name = "components/formularios/lotes/lote_form.html"
    form_class = LoteForm
    success_url = reverse_lazy("dashboard:dashboard_home")


# Vista para eliminar un lote
class LoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Lote
    template_name = "components/confirmaciones/lotes/lote_confirm_delete.html"
    success_url = reverse_lazy("dashboard:dashboard_home")
    
    
# ============================================================
# Vistas para SimsCard
# ============================================================

# Vista para listar las SIMCards de un lote específico
class SimCardListView(LoginRequiredMixin, ListView):
    model = SimCard
    template_name = "pages/simcards_list.html" # Crea este template
    context_object_name = "simcards"

    def get_queryset(self):
        # Filtra las SIMCards por el lote pasado en la URL
        lote_pk = self.kwargs['pk']
        return SimCard.objects.filter(id_lote__pk=lote_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega el lote al contexto para usarlo en el template
        context['lote'] = Lote.objects.get(pk=self.kwargs['pk'])
        return context

# Vista para crear una nueva SIMCard en un lote específico
class SimCardCreateView(LoginRequiredMixin, CreateView):
    model = SimCard
    template_name = "components/formularios/simscards/simscards_form.html"
    form_class = SimCardForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lote'] = Lote.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        lote_pk = self.kwargs['pk']
        return reverse_lazy('dashboard:simcard_list', kwargs={'pk': lote_pk})

    def form_valid(self, form):
        lote_pk = self.kwargs['pk']
        lote = Lote.objects.get(pk=lote_pk)
        
        # Asigna el lote y el usuario propietario
        form.instance.id_lote = lote
        # form.instance.id_usuario_propietario = self.request.user # Si existe este campo
        
        return super().form_valid(form)

# Vista para actualizar una SIMCard existente
class SimCardUpdateView(LoginRequiredMixin, UpdateView):
    model = SimCard
    template_name = "components/formularios/simscards/simscards_form.html"
    form_class = SimCardForm
    
    def get_success_url(self):
        # Redirige a la lista de SIMCards del lote actual
        simcard = self.get_object()
        lote_pk = simcard.id_lote.pk
        return reverse_lazy('dashboard:simcard_list', kwargs={'pk': lote_pk})

# Vista para eliminar una SIMCard
class SimCardDeleteView(LoginRequiredMixin, DeleteView):
    model = SimCard
    template_name = "components/confirmaciones/simscards/simcard_confirm_delete.html"
    
    def get_success_url(self):
        # Redirige a la lista de SIMCards del lote actual
        simcard = self.get_object()
        lote_pk = simcard.id_lote.pk
        return reverse_lazy('dashboard:simcard_list', kwargs={'pk': lote_pk})