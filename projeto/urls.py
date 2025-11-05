from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('rendamensal/', include('projeto.rendamensal.urls', namespace='rendamensal')),
    path('despesas/', include('projeto.despesas.urls', namespace='despesas')),
    path('financiamentos/', include('projeto.financiamentos.urls', namespace='financiamentos')),
]