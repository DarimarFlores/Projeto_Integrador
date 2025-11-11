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
]