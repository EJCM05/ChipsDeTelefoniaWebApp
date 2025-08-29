"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

app_name = "dashboard"

urlpatterns = [
    # renderizado Pages
    path("dashboardHome/", LoteListView.as_view(), name="dashboard_home"),
    path("dashboardClientes/", ViewClientes.as_view(), name="dashboard_clientes"),
    path("dashboardPerfil/", dashboard_perfil, name="dashboard_perfil"),
    path("dashboardEstadisticas/", dashboard_estadisticas, name="dashboard_estadisticas"),
    path("dashboardVentas/", ListaVentasView.as_view(), name="dashboard_ventas"),
    path("dashboardReportes/", ListaReportesView.as_view(), name="dashboard_reportes"),
    path("dashboardOperadoras/", OperadoraListView.as_view(), name="dashboard_operadoras"),
    
    # CBVS
    path("logout/", LogoutView.as_view(), name="logout"),

    # CRUD para lotes
    path("lotes/crear/", LoteCreateView.as_view(), name="lote_create"),
    path("lotes/<int:pk>/editar/", LoteUpdateView.as_view(), name="lote_update"),
    path("lotes/<int:pk>/eliminar/", LoteDeleteView.as_view(), name="lote_delete"),

    # Crud para SimsCards (dependen del lote)
    path("lotes/<int:pk>/simcards/", SimCardListView.as_view(), name="simcard_list"),
    path("lotes/<int:pk>/simcards/crear/", SimCardCreateView.as_view(), name="simcard_create"),
    path("simcards/<int:pk>/editar/", SimCardUpdateView.as_view(), name="simcard_update"),
    path("simcards/<int:pk>/eliminar/", SimCardDeleteView.as_view(), name="simcard_delete"),

    # CRUD para Operadoras
    path("operadoras/crear/", OperadoraCreateView.as_view(), name="operadora_create"),
    path("operadoras/<int:pk>/editar/", OperadoraUpdateView.as_view(), name="operadora_update"),
    path("operadoras/<int:pk>/eliminar/", OperadoraDeleteView.as_view(), name="operadora_delete"),
    
    # CRUD para ventas
    path('generar-venta/', GenerarVentaView.as_view(), name='generar_venta'),
    path('detalle-venta/<int:pk>/', DetalleVentaView.as_view(), name='detalle_venta'),
    path('editar-venta/<int:pk>/', EditarVentaView.as_view(), name='editar_venta'),

    # Funcion para generar excel estadisticas
    path('reporte_lotes/', generar_reporte_lotes_excel, name='reporte_lotes_excel'),

    # Funcion de la grafica
    path('api/ventas/<int:year>/', obtener_ventas, name='ventas_data'),

    # Funciones Auxiliares Ajax
    path('ajax/load-simcards/', get_simcards_by_lote, name='ajax_load_simcards'),

]
