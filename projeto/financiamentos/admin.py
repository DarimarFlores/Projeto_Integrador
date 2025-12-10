from django.contrib import admin
from .models import Financiamento

@admin.register(Financiamento)
class Financiamentos(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'mes', 'credor', 'tipo', 'valor_parcela', 'data_vencimento', 'pago')
    list_filter = ('usuario', 'mes', 'tipo','pago')
    search_fields = ('usuario__username', 'credor')
