from django.urls import path
from .views import LoginCustomView, registrar, logout_view, esqueci_senha, trocar_senha
from . import views

app_name = 'contas'

urlpatterns = [
    path('login/', LoginCustomView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registrar/', registrar, name='registrar'),
    path('esqueci-senha/', views.esqueci_senha, name='esqueci_senha'),
    path('trocar-senha/', views.trocar_senha, name='trocar_senha'),
]