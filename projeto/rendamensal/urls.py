from django.urls import path
from . import views

app_name = 'rendamensal'   

urlpatterns = [
    path('', views.cadastroRenda, name='cadastro_renda'), 
    path('nova/', views.nova_renda, name='nova_renda'),            
    path('editar/<int:id>/', views.editar_renda, name='editar_renda'), 
    path('remover/<int:id>/', views.remover_renda, name='remover_renda'), 
]