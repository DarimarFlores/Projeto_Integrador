from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('meta_poupanca/', views.meta_poupanca, name='meta_poupanca'),
    path('rendamensal/', include('projeto.rendamensal.urls', namespace='rendamensal')),
    path('despesas/', include('projeto.despesas.urls', namespace='despesas')),
    path('financiamentos/', include('projeto.financiamentos.urls', namespace='financiamentos')),
    path('contas/', include('projeto.contas.urls', namespace='contas')),
    path('relatorios/mensal/', views.relatorio_mensal, name='relatorio_mensal'),
    path('alertas/', views.alertas, name='alertas'),
]