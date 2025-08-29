from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import re
from django.contrib.auth import logout



class AdminReauthMiddleware:
    """
    Middleware que fuerza la re-autenticación para acceder a cualquier
    página del panel de administración de Django.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_url_pattern = re.compile(r'^/admin/.*$')

    def __call__(self, request):
        # Ignora la petición si el usuario ya está en la página de login del admin
        # o si es la página de logout.
        if request.path.startswith(reverse('admin:login')) or request.path.startswith(reverse('admin:logout')):
            return self.get_response(request)

        # Si el usuario intenta acceder a cualquier URL del admin y ya está autenticado...
        if self.admin_url_pattern.match(request.path) and request.user.is_authenticated:
            # Desconecta la sesión del usuario.
            logout(request)

            # Redirige a la página de login del admin.
            # Puedes pasar un parámetro 'next' para que el usuario sea
            # redirigido a la página que intentaba acceder después de loguearse de nuevo.
            return redirect(f"{reverse('admin:login')}?next={request.path}")
        
        # Para todas las demás peticiones, continúa con el flujo normal.
        return self.get_response(request)