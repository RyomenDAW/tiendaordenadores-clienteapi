from django.urls import path, re_path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
# urls.py
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.inicio, name ='inicio'),
    path('', views.inicio, name='inicio'),  # Página de inicio
    #==================================================================================================================================================
    

    path('template-api/procesador_list.html', views.procesadores_lista_api, name='procesadores_lista_api'),
    path('template-api/procesador_list_mejorado.html', views.procesadores_lista_mejorada_api, name='procesadores_lista_mejorada_api'),
    path('template-api/grafica_list.html', views.graficas_lista_api, name='graficas_lista_api'),
    path('template-api/fuente_list.html', views.fuentes_lista_api, name='fuentes_lista_api'),
    path('template-api/ram_list.html', views.rams_lista_api, name='rams'),  # Ruta para la lista de RAMs
    path('template-api/placasbase_list.html', views.placasbase_lista_api, name='placasbase'),
    path('procesadores-mejorados', views.procesador_busqueda_simple, name='procesadores-mejorados'),
    
    
    
    path('procesador_busqueda/', views.procesador_busqueda_simple, name='procesador_busqueda'),
    path('procesador_busqueda_avanzada/', views.procesador_busqueda_avanzada, name='procesador_busqueda_avanzada'),


    # Rutas para el template de búsqueda avanzada (formularios)
    path('template-api/grafica_busqueda_avanzada/', views.grafica_busqueda_avanzada, name='grafica_busqueda_avanzada'),
    path('template-api/fuente_busqueda_avanzada/', views.fuente_busqueda_avanzada, name='fuente_busqueda_avanzada'),
    path('template-api/ram_busqueda_avanzada/', views.ram_busqueda_avanzada, name='ram_busqueda_avanzada'),
    #==================================================================================================================================================
    path('procesadores/crear/', views.crear_procesador, name='crear_procesador'),

    # path('registrar',views.registrar_usuario, name='registrar_usuario'),
    # path('logout/', LogoutView.as_view(), name='logout'),  # Ruta para el logout
    # path('libros/busqueda_simple',views.libro_busqueda_simple,name='libro_buscar_simple'),
]