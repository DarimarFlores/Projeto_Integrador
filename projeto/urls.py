from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps com namespace (suas apps estão dentro de "projeto")
    path(
        'rendamensal/',
        include(('projeto.rendamensal.urls', 'rendamensal'), namespace='rendamensal')
    ),
    path(
        'despesas/',
        include(('projeto.despesas.urls', 'despesas'), namespace='despesas')
    ),
]