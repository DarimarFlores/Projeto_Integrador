from django.urls import path
from . import views

urlpatterns =[
    path('', views.lista_despesas, name= 'lista_despesas'),
    path('nova/', views.nova_despesa, name= 'nova_despesa'),
    path('editar/<int:id>/', views.editar_despesa, name='editar_despesa'),
    path('remove/<int:id>/',views.remover_despesa, name='remover_despesa'),
]