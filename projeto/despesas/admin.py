from django.contrib import admin
from .models import Despesa

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'mes', 'nome', 'valor', 'data_vencimento', 'pago')
    list_filter = ('usuario', 'mes', 'pago', 'tipo')
    search_fields = ('usuario__username', 'nome')
