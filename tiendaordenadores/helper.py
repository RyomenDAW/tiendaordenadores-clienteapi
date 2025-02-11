import requests
import os  # Para obtener el token de acceso desde las variables de entorno
import environ
from django.shortcuts import render, redirect
from .forms import *
from requests.exceptions import HTTPError, RequestException
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  # <- Se invoca después de inicializar `env`


class helper:
    @staticmethod
    def obtener_placasbases_select():
        # Obtener el token de acceso desde .env
        access_token = env("ACCESS_TOKEN")

        print("🔑 Token que se enviará:", access_token)

        # Definir los headers con el token de acceso
        headers = {'Authorization': f'Bearer {access_token}'}
        
        url = 'http://127.0.0.1:8000/api/v1/placasbase'

        # Hacer la petición GET a la API
        response = requests.get(url, headers=headers)

        # Mostrar qué se está enviando
        print("📡 Headers enviados:", headers)
        print("🔎 Código de respuesta:", response.status_code)
        print("🔎 Respuesta de la API:", response.text)

        # Convertir la respuesta a JSON
        placasbases = response.json()

        # Construir la lista de opciones con ID y nombre
        lista_placasbases = [("", "Ninguna")]  # Permitir una opción vacía
        for placabase in placasbases:
            lista_placasbases.append((placabase["id"], placabase["nombre"]))

        return lista_placasbases
