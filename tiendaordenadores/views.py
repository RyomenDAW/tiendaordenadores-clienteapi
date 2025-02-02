from django.shortcuts import render
from django.core import serializers
import requests

def procesadores_lista_api(request):
    #Obtenemos todos los procesadores
    headers = {'Authorization': 'Bearer eaf4cUG1YB6UP7eesuD87eCDnNY0wd'}
    response = requests.get('http://127.0.0.1:8000/api/v1/procesadores', headers = headers)
    #Transformamos la respuesta en json
    procesadores = response.json()
    return render(request, 'template-api/procesador_list.html',{"procesadores_mostrar":procesadores})

def procesadores_lista_mejorada_api(request):
    # Obtenemos todos los procesadores con información de la marca relacionada y user.
    headers = {'Authorization': 'Bearer eaf4cUG1YB6UP7eesuD87eCDnNY0wd'}
    response = requests.get('http://127.0.0.1:8000/api/v1/procesadores-mejorados', headers=headers)
    # Transformamos la respuesta en JSON
    procesadores = response.json()
    return render(request, 'template-api/procesador_list_mejorado.html', {"procesadores_mostrar": procesadores})



#Esta de aqui es mejorada
def graficas_lista_api(request):
    headers = {'Authorization': 'Bearer eaf4cUG1YB6UP7eesuD87eCDnNY0wd'}
    response = requests.get('http://127.0.0.1:8000/api/v1/graficas', headers=headers)
    graficas = response.json()
    return render(request, 'template-api/grafica_list.html', {"graficas_mostrar": graficas})

#Esta de aqui es mejorada
def fuentes_lista_api(request):
    headers = {'Authorization': 'Bearer eaf4cUG1YB6UP7eesuD87eCDnNY0wd'}
    response = requests.get('http://127.0.0.1:8000/api/v1/fuentes', headers=headers)
    fuentes = response.json()
    return render(request, 'template-api/fuente_list.html', {"fuentes_mostrar": fuentes})


#Esta de aqui es mejorada
def rams_lista_api(request):
    headers = {'Authorization': 'Bearer eaf4cUG1YB6UP7eesuD87eCDnNY0wd'}
    # Realizamos la solicitud GET a la URL de la API donde se encuentran las RAMs
    response = requests.get('http://127.0.0.1:8000/api/v1/rams', headers=headers)
    # Transformamos la respuesta en JSON
    rams = response.json()
    
    # Renderizamos la respuesta en una plantilla
    return render(request, 'template-api/ram_list.html', {"rams_mostrar": rams})
#Nosotros hemos conseguido este token a d9e6da5bb6564fd1b638ed7a802c2184 gracias a OIDC




