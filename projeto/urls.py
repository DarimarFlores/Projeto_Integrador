from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('rendamensal/', include('projeto.rendamensal.urls', namespace='rendamensal')),
    path('despesas/', include('projeto.despesas.urls', namespace='despesas')),
]