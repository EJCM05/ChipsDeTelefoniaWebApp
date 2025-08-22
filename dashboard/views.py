
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView,FormView,DetailView)
from core.models import *
from django.shortcuts import render, redirect, get_object_or_404
from .urls import *
from .forms import *
from django.http import JsonResponse

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

def dashboard_operadoras(request):
    return render(request, "pages/operadoras.html")

# ==========================================================
#               Clases para Lotes
# ==========================================================
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
#            Clases para SIMCards
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
    
# ======================================================================
#               Clases para Operadoras 
# ======================================================================
    
class OperadoraListView(LoginRequiredMixin, ListView):
    model = Operadora
    template_name = "components/tablas/operadoras/operadora_list.html"
    context_object_name = "operadoras"

# Vista para crear una nueva operadora
class OperadoraCreateView(LoginRequiredMixin, CreateView):
    model = Operadora
    template_name = "components/formularios/operadoras/operadoras_form.html"
    form_class = OperadoraForm
    success_url = reverse_lazy("dashboard:dashboard_operadoras")

# Vista para actualizar una operadora existente
class OperadoraUpdateView(LoginRequiredMixin, UpdateView):
    model = Operadora
    template_name = "components/formularios/operadoras/operadoras_form.html"
    form_class = OperadoraForm
    success_url = reverse_lazy("dashboard:dashboard_operadoras")

# Vista para eliminar una operadora
class OperadoraDeleteView(LoginRequiredMixin, DeleteView):
    model = Operadora
    template_name = "components/confirmaciones/operadoras/operadoras_confirm_delete.html"
    success_url = reverse_lazy("dashboard:dashboard_operadoras")
    
# ==========================================================================
                    # Clases ventas
# ==========================================================================

class GenerarVentaView(LoginRequiredMixin, FormView):
    template_name = 'components/formularios/ventas/formulario_ventas.html'
    form_class = VentaForm
    success_url = reverse_lazy('dashboard:dashboard_ventas')

    
    def form_valid(self, form):
        print("El método form_valid se ha ejecutado correctamente.")

        # 1. Crear el nuevo Cliente
        nuevo_cliente = Cliente(
            # CAMBIO: Usar form.cleaned_data
            primer_nombre=form.cleaned_data['primer_nombre'],
            segundo_nombre=form.cleaned_data['segundo_nombre'],
            primer_apellido=form.cleaned_data['primer_apellido'],
            segundo_apellido=form.cleaned_data['segundo_apellido'],
            cedula_identidad=form.cleaned_data['cedula_identidad'],
            fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
            telefono=form.cleaned_data['telefono'], # <-- AQUI ESTABA EL ERROR
            correo=form.cleaned_data['correo'],     # <-- AQUI ESTABA EL ERROR
            id_usuario_propietario=self.request.user
        )
        nuevo_cliente.save()

        # 2. Obtener la SIM Card seleccionada y actualizar su estado
        simcard_seleccionada = form.cleaned_data['simcard']
        simcard_seleccionada.estado = 'vendida'
        simcard_seleccionada.id_cliente = nuevo_cliente
        simcard_seleccionada.numero_telefono = form.cleaned_data['telefono']
        simcard_seleccionada.save()

        # 3. Crear la nueva Venta
        Venta.objects.create(
            id_cliente=nuevo_cliente,
            id_simcard=simcard_seleccionada,
            id_usuario_propietario=self.request.user,
            monto_total=10.00
        )
        
        return redirect(self.success_url)
    
# Vista para listar las ventas (reportes)
class ListaVentasView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'pages/ventas.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        # Opcional: Muestra solo las ventas del usuario actual si es supervisor
        if self.request.user.rol == 'supervisor':
            return Venta.objects.filter(id_usuario_propietario=self.request.user).order_by('-fecha_venta')
        return Venta.objects.all().order_by('-fecha_venta')

# Vista de detalle para ver una factura/reporte individual
class DetalleVentaView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'components/tablas/ventas/detalles_reportes.html'
    context_object_name = 'venta'
    
    def get_queryset(self):
        # Asegura que un supervisor solo pueda ver sus propias ventas
        if self.request.user.rol == 'supervisor':
            return Venta.objects.filter(id_usuario_propietario=self.request.user)
        return Venta.objects.all()
    
# ==========================================================================
                # Clase Reportes de ventas
# ==========================================================================


class ListaReportesView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'pages/reportes.html'
    context_object_name = 'ventas'
    paginate_by = 10 # Número de ventas por página

    def get_queryset(self):
        # Asegura que las ventas se muestren de la más reciente a la más antigua
        # y filtra por el usuario si es un supervisor
        queryset = Venta.objects.all().order_by('-fecha_venta')

        # Restringe los reportes si el usuario no es un administrador
        if self.request.user.rol == 'supervisor':
            queryset = queryset.filter(id_usuario_propietario=self.request.user)

        return queryset


# Funciones auxiliares Ajax para Las simscards
def get_simcards_by_lote(request):
    """
    Vista que devuelve una lista de SIM Cards disponibles
    (estado 'inactiva') para un lote específico, en formato JSON.
    """
    if request.method == 'GET' and 'lote_id' in request.GET:
        try:
            lote_id = request.GET.get('lote_id')
            simcards = SimCard.objects.filter(id_lote=lote_id).exclude(estado='vendida')
            
            data = [
                {
                'id': simcard.id,
                'codigo': simcard.codigo,
                'estado': simcard.estado
                }
                for simcard in simcards
            ]
            return JsonResponse({'simcards': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Petición inválida'}, status=400)