from django.urls import path
from . import views

urlpatterns = [
    path ('', views.cadastro_renda, name='cadastro_renda'),
]