from django.urls import path
from . import views

app_name = 'financiamentos'

urlpatterns = [
    path('', views.lista_financiamentos, name='lista_financiamentos'),
    path('novo/', views.novo_financiamento, name='novo_financiamento'),
    path('editar/<int:id>/', views.editar_financiamento, name='editar_financiamento'),
    path('remover/<int:id>/', views.remover_financiamento, name='remover_financiamento'),
]