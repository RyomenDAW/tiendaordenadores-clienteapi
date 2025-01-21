from django.shortcuts import render
from django.core import serializers
import requests

def procesadores_lista_api(request):
    #Obtenemos todos los procesadores
    response = requests.get('http://127.0.0.1:8000/api/v1/procesadores')
    #Transformamos la respuesta en json
    procesadores = response.json()
    return render(request, 'template-api/procesador_list.html',{"procesadores_mostrar":procesadores})