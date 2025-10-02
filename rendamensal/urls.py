from django.urls import path
from . import views

urlpatterns = [
    path ('', views.cadastro_renda, name='cadastro_renda'),
    path('editar/<int:id>/', views.editar_renda, name='editar_renda'),
    path('remover/<int:id>/', views.remover_renda, name='remover_renda'),
]