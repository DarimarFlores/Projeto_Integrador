from django.contrib import admin
from .models import Renda

@admin.register(Renda)
class RendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'mes', 'tipo', 'valor', 'data_recebimento')
    list_filter = ('usuario', 'mes', 'tipo')
    search_fields = ('usuario__username',)
