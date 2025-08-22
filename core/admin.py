from django.contrib import admin

from .models import *

# Register your models here.
admin.site.site_header = "Chips de Telefonia"
admin.site.site_title = "Chips de Telefonía"
admin.site.index_title = "Panel de Administración"
admin.site.register(Usuario)
admin.site.register(Operadora)
admin.site.register(Lote)
admin.site.register(Cliente)
admin.site.register(SimCard)
admin.site.register(Venta)