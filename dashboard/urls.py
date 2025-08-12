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
    path("dashboardClientes/", dashboard_clientes, name="dashboard_clientes"),
    path("dashboardPerfil/", dashboard_perfil, name="dashboard_perfil"),
    path("dashboardEstadisticas/", dashboard_estadisticas, name="dashboard_estadisticas"),
    path("dashboardVentas/", dashboard_ventas, name="dashboard_ventas"),
    path("dashboardReportes/", dashboard_reportes, name="dashboard_reportes"),
    
    
    # CBVS
    path("logout/", LogoutView.as_view(), name="logout"),

    # CRUD para lotes
    path("lotes/crear/", LoteCreateView.as_view(), name="lote_create"),
    path("lotes/<int:pk>/editar/", LoteUpdateView.as_view(), name="lote_update"),
    path("lotes/<int:pk>/eliminar/", LoteDeleteView.as_view(), name="lote_delete"),

    # Crud para SimsCards
    # URLs para el CRUD de SIMCards (ahora dependen del lote)
    path("lotes/<int:pk>/simcards/", SimCardListView.as_view(), name="simcard_list"),
    path("lotes/<int:pk>/simcards/crear/", SimCardCreateView.as_view(), name="simcard_create"),
    path("simcards/<int:pk>/editar/", SimCardUpdateView.as_view(), name="simcard_update"),
    path("simcards/<int:pk>/eliminar/", SimCardDeleteView.as_view(), name="simcard_delete"),
]
