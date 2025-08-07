from django.shortcuts import render
from .urls import *

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

