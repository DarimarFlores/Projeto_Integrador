from django.urls import path
from .views import LoginCustomView, registrar, logout_view

app_name = 'contas'

urlpatterns = [
    path('login/', LoginCustomView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registrar/', registrar, name='registrar'),
]