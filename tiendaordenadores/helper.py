import requests
import os
import json
import environ
from pathlib import Path

# Configuración de variables de entorno
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  # Cargar variables de entorno

# URL base de la API para Procesadores, Gráficas y Monitores-Graficas
API_PROCESADORES_URL = "http://127.0.0.1:8000/template-api/procesadores/"
API_GRAFICAS_URL = "http://127.0.0.1:8000/template-api/graficas/"
API_MONITORES_GRAFICAS_URL = "http://127.0.0.1:8000/template-api/monitores-graficas/"

class helper:
    @staticmethod
    def obtener_token():
        """ Obtiene el token de acceso desde el archivo .env """
        token = env("ACCESS_TOKEN", default=None)
        if not token:
            print("⚠️ ADVERTENCIA: No se encontró el token de acceso en el archivo .env")
        return token

    @staticmethod
    def api_request(method, endpoint, data=None, tipo="procesador"):
        """
        Método genérico para hacer peticiones a la API con autenticación.
        - `tipo="procesador"` -> Usará la URL de procesadores.
        - `tipo="grafica"` -> Usará la URL de gráficas.
        - `tipo="monitores-graficas"` -> Usará la URL de monitores-graficas.
        """

        token = helper.obtener_token()
        if not token:
            print("❌ ERROR: No se puede continuar sin un token válido.")
            return None

        headers = {
            'Authorization': 'Token ' + token,  
            'Content-Type': 'application/json'
        }

        # 🔥 **Corrección en la selección de URL**
        api_urls = {
            "procesador": API_PROCESADORES_URL,
            "grafica": API_GRAFICAS_URL,
            "monitores-graficas": API_MONITORES_GRAFICAS_URL
        }

        if tipo not in api_urls:
            print(f"❌ ERROR: Tipo de API desconocido: {tipo}")
            return None

        url = f"{api_urls[tipo].rstrip('/')}/{endpoint.lstrip('/')}"

        print(f"📡 Enviando solicitud {method.upper()} a {url}")
        print(f"🔑 Token utilizado: {token[:10]}... (oculto por seguridad)")

        try:
            response = requests.request(method, url, headers=headers, json=data)
            print(f"🔎 Respuesta {response.status_code}: {response.text}")

            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 404:
                print(f"🚨 ERROR 404: No se encontró el endpoint {url}.")
        except requests.RequestException as e:
            print(f"❌ ERROR en la solicitud: {str(e)}")

        return None

    ## ==============================
    ## 🚀 PROCESADORES (CRUD) 🚀
    ## ==============================

    @staticmethod
    def obtener_procesador(procesador_id):
        return helper.api_request("get", f"{procesador_id}/", tipo="procesador")

    @staticmethod
    def actualizar_procesador(procesador_id, datos):
        return helper.api_request("put", f"{procesador_id}/", data=datos, tipo="procesador")

    @staticmethod
    def actualizar_nombre_procesador(procesador_id, nuevo_nombre):
        return helper.api_request("patch", f"{procesador_id}/actualizar-nombre/", data={"nombre": nuevo_nombre}, tipo="procesador")

    @staticmethod
    def eliminar_procesador(procesador_id):
        return helper.api_request("delete", f"{procesador_id}/", tipo="procesador")

    ## ==============================
    ## 🎨 GRÁFICAS (CRUD) 🎨
    ## ==============================

    @staticmethod
    def obtener_grafica(grafica_id):
        return helper.api_request("get", f"{grafica_id}/", tipo="grafica")

    @staticmethod
    def actualizar_grafica(grafica_id, datos):
        return helper.api_request("put", f"{grafica_id}/", data=datos, tipo="grafica")

    @staticmethod
    def actualizar_nombre_grafica(grafica_id, nuevo_nombre):
        return helper.api_request("patch", f"{grafica_id}/actualizar-nombre/", data={"nombre": nuevo_nombre}, tipo="grafica")

    @staticmethod
    def eliminar_grafica(grafica_id):
        return helper.api_request("delete", f"{grafica_id}/eliminar/", tipo="grafica")

    ## ==============================
    ## 🖥️ MONITOR-GRAFICA (ManyToMany CRUD) 🖥️
    ## ==============================

    @staticmethod
    def crear_monitor_grafica(monitor_id, grafica_id, modo_conexion, es_monitor_gaming=False, resolucion_maxima=1080):
        """ Crea una relación Monitor-Grafica con validaciones """
        datos = {
            "monitor": monitor_id,
            "grafica": grafica_id,
            "modo_conexion": modo_conexion,
            "es_monitor_gaming": es_monitor_gaming,
            "resolucion_maxima": resolucion_maxima
        }
        return helper.api_request("post", "crear/", data=datos, tipo="monitores-graficas")

    @staticmethod
    def actualizar_monitor_grafica(relacion_id, monitor_id=None, grafica_id=None, modo_conexion=None, resolucion_maxima=None):
        """ Actualiza una relación Monitor-Grafica """
        datos = {}
        if monitor_id:
            datos["monitor"] = monitor_id
        if grafica_id:
            datos["grafica"] = grafica_id
        if modo_conexion:
            datos["modo_conexion"] = modo_conexion
        if resolucion_maxima:
            datos["resolucion_maxima"] = resolucion_maxima

        return helper.api_request("put", f"{relacion_id}/editar/", data=datos, tipo="monitores-graficas")

    @staticmethod
    def actualizar_grafica_en_relacion(relacion_id, nueva_grafica_id):
        """ Actualiza solo la tarjeta gráfica en una relación Monitor-Grafica """
        datos = {"grafica": nueva_grafica_id}
        return helper.api_request("patch", f"{relacion_id}/actualizar-grafica/", data=datos, tipo="monitores-graficas")

    @staticmethod
    def eliminar_monitor_grafica(relacion_id):
        """ Elimina una relación Monitor-Grafica """
        return helper.api_request("delete", f"{relacion_id}/eliminar/", tipo="monitores-graficas")


import requests

API_TOKEN_URL = "http://127.0.0.1:8000/oauth2/token/"

def obtener_token_session(username, password):
    """Obtiene el token de acceso desde la API REST usando OAuth2"""
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': 'tiendaordenadores',  # Sustituir con el ID si cambia
        'client_secret': 'tiendaordenadores'  # Sustituir con el Secret real
    }

    response = requests.post(API_TOKEN_URL, data=data)
    respuesta = response.json()

    if response.status_code == 200:
        return respuesta.get('access_token')
    else:
        raise Exception(respuesta.get("error_description", "Error al obtener el token"))
