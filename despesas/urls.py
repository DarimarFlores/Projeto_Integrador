from django.urls import path
from . import views

urlpatterns =[
    path('', views.lista_despesas, name= 'lista_despesas'),
    path('nova/', views.nova_despesa, name= 'nova_despesa'),
]