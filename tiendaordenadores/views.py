from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
from requests.exceptions import HTTPError

import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


#ESTA ES LA PAGINA INDEX, AQUI IRA TODAN LAS URLS, EN TOTAL 10.
def inicio(request):
    return render(request, 'home/index.html')


def procesadores_lista_api(request):
    #Obtenemos todos los procesadores
    headers = {'Authorization': 'Bearer ps7p9WY8tIgq63lpE1YNj3dk8dYyQE'}
    response = requests.get('http://127.0.0.1:8000/api/v1/procesadores', headers = headers)
    #Transformamos la respuesta en json
    procesadores = response.json()
    return render(request, 'template-api/procesador_list.html',{"procesadores_mostrar":procesadores})

def procesadores_lista_mejorada_api(request):
    # Obtenemos todos los procesadores con información de la marca relacionada y user.
    headers = {'Authorization': 'Bearer ps7p9WY8tIgq63lpE1YNj3dk8dYyQE'}
    response = requests.get('http://127.0.0.1:8000/api/v1/procesadores-mejorados', headers=headers)
    # Transformamos la respuesta en JSON
    procesadores = response.json()
    return render(request, 'template-api/procesador_list_mejorado.html', {"procesadores_mostrar": procesadores})



#Esta de aqui es mejorada
def graficas_lista_api(request):
    headers = {'Authorization': 'Bearer ps7p9WY8tIgq63lpE1YNj3dk8dYyQE'}
    response = requests.get('http://127.0.0.1:8000/api/v1/graficas', headers=headers)
    graficas = response.json()
    return render(request, 'template-api/grafica_list.html', {"graficas_mostrar": graficas})

#Esta de aqui es mejorada
def fuentes_lista_api(request):
    headers = {'Authorization': 'Bearer ps7p9WY8tIgq63lpE1YNj3dk8dYyQE'}
    response = requests.get('http://127.0.0.1:8000/api/v1/fuentes', headers=headers)
    fuentes = response.json()
    return render(request, 'template-api/fuente_list.html', {"fuentes_mostrar": fuentes})


#Esta de aqui es mejorada
def rams_lista_api(request):
    headers = {'Authorization': 'Bearer ps7p9WY8tIgq63lpE1YNj3dk8dYyQE'}
    # Realizamos la solicitud GET a la URL de la API donde se encuentran las RAMs
    response = requests.get('http://127.0.0.1:8000/api/v1/rams', headers=headers)
    # Transformamos la respuesta en JSON
    rams = response.json()
    
    # Renderizamos la respuesta en una plantilla
    return render(request, 'template-api/ram_list.html', {"rams_mostrar": rams})
#Nosotros hemos conseguido este token a d9e6da5bb6564fd1b638ed7a802c2184 gracias a OIDC



def crear_cabecera():
    return {'Authorization': 'Bearer ps7p9WY8tIgq63lpE1YNj3dk8dYyQE',
    "Content-Type": "application/json"}


#Views.py de cliente API, no API REST
def procesador_busqueda_simple(request):
    formulario = BusquedaProcesadorSimple(request.GET)
    print(request.GET)  # Imprimir los parámetros de la solicitud
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/procesadores',
            headers=headers,
            params={'textoBusqueda': formulario.data.get("textoBusqueda")}    
        )
        procesadores = response.json()
        return render(request, 'procesadores/lista_procesadores.html', {"procesadores": procesadores})

    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect('inicio')





# def libro_busqueda_simple(request):
#     formulario = BusquedaLibroForm(request.GET)
    
#     if formulario.is_valid():
#         headers = crear_cabecera()
#         response = requests.get(
#             'http://127.0.0.1:8000/api/v1/libros/busqueda_simple',
#             headers=headers,
#             params={'textoBusqueda':formulario.data.get("textoBusqueda")}
#         )
#         libros = response.json()
#         return render(request, 'libro/lista_mejorada.html',{"libros_mostrar":libros})
#     if("HTTP_REFERER" in request.META):
#         return redirect(request.META["HTTP_REFERER"])
#     else:
#         return redirect("index")