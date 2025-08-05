from django.shortcuts import render

from .urls import *


def dashboard_home(request):
    return render(request, "pages/dashboard_home.html")


# Create your views here.
