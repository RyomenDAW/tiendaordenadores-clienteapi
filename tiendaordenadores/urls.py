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
    path('template-api/procesador_list_mejorado.html', views.procesadores_lista_mejorada_api, name='procesadores_lista_mejorada_api')

]