from django.shortcuts import render
from django.core import serializers
import requests

def procesadores_lista_api(request):
    #Obtenemos todos los procesadores
    headers = {'Authorization': 'Bearer sfTTDSS3wekREQ3lAJ5sBcR07JOxVx'}
    response = requests.get('http://127.0.0.1:8000/api/v1/procesadores', headers = headers)
    #Transformamos la respuesta en json
    procesadores = response.json()
    return render(request, 'template-api/procesador_list.html',{"procesadores_mostrar":procesadores})

def procesadores_lista_mejorada_api(request):
    # Obtenemos todos los procesadores con información de la marca relacionada
    headers = {'Authorization': 'Bearer sfTTDSS3wekREQ3lAJ5sBcR07JOxVx'}
    response = requests.get('http://127.0.0.1:8000/api/v1/procesadores-mejorados', headers=headers)
    # Transformamos la respuesta en JSON
    procesadores = response.json()
    return render(request, 'template-api/procesador_list_mejorado.html', {"procesadores_mostrar": procesadores})
