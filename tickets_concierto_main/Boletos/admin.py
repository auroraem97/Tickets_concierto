from django.contrib import admin
from .models import Categoria, Concierto,TipoBoleto, Compra

admin.site.register(Categoria)
admin.site.register(Concierto)
admin.site.register(TipoBoleto)
admin.site.register(Compra)