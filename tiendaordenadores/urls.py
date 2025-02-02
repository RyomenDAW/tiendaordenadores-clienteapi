from django.urls import path, re_path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
# urls.py
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('template-api/procesador_list.html', views.procesadores_lista_api, name='procesadores_lista_api'),
    path('template-api/procesador_list_mejorado.html', views.procesadores_lista_mejorada_api, name='procesadores_lista_mejorada_api'),
    path('template-api/grafica_list.html', views.graficas_lista_api, name='graficas_lista_api'),
    path('template-api/fuente_list.html', views.fuentes_lista_api, name='fuentes_lista_api'),
    path('template-api/ram_list.html', views.rams_lista_api, name='rams'),  # Ruta para la lista de RAMs

]