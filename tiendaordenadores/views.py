from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
from requests.exceptions import HTTPError

import requests
import environ
import os
from pathlib import Path



# Configuración de variables de entorno
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

# Obtener la versión de la API desde settings.py
api_base_url = "http://127.0.0.1:8000/"
version = env('API_VERSION')  # Lee la versión de la API desde el archivo .env






from requests.exceptions import HTTPError, RequestException

# Esta función se encarga de manejar los errores de las peticiones a la API
def manejar_errores(request, response, formulario, template):
    try:
        # Si la respuesta tiene un código de error (no es 200 OK)
        response.raise_for_status()

    except HTTPError as http_err:
        # Si hay un error HTTP (como 400, 404, etc.)
        print(f'Hubo un error en la petición: {http_err}')
        
        # Manejar el error: si es un error 400 (bad request), obtenemos los errores
        if response.status_code == 400:
            errores = response.json()  # Los errores vienen en formato JSON
            for error in errores:
                # Añadimos los errores al formulario para mostrar al usuario
                formulario.add_error(error, errores[error])

            # Retornamos la vista con el formulario y los errores
            return render(request, template, {"formulario": formulario, "errores": errores})
        else:
            # Si el error no es 400, podemos redirigir a un error genérico 500
            return mi_error_500(request)

    except RequestException as req_err:
        # Si hay un error en la conexión (por ejemplo, no se puede conectar a la API)
        print(f'Error de conexión: {req_err}')
        return mi_error_500(request)

    except Exception as err:
        # Si hay un error inesperado
        print(f'Ocurrió un error inesperado: {err}')
        return mi_error_500(request)




#ESTA ES LA PAGINA INDEX, AQUI IRA TODAN LAS URLS, EN TOTAL 10.
def inicio(request):
    return render(request, 'home/index.html')


def mi_error_404(request, exception=None):
    # ERROR 404: NO SE ENCUENTRA LA PÁGINA SOLICITADA.
    return render(request, 'errores/404.html', None, None, 404)

def mi_error_400(request, exception=None):
    # ERROR 400: SOLICITUD INCORRECTA, GENERALMENTE DEBIDO A UN MAL FORMATO.
    return render(request, 'errores/400.html', None, None, 400)

def mi_error_403(request, exception=None):
    # ERROR 403: ACCESO PROHIBIDO, NO TIENE PERMISOS PARA VER ESTE RECURSO. (ADMIN)
    return render(request, 'errores/403.html', None, None, 403)

def mi_error_500(request, exception=None):
    # ERROR 500: ERROR INTERNO DEL SERVIDOR, OCURRE CUANDO HAY UN PROBLEMA NO ESPECIFICADO.
    return render(request, 'errores/500.html', None, None, 500)



# Obtener los formatos de la API desde el archivo .env
api_formatos = json.loads(env('API_FORMATOS'))  # Convertimos la cadena JSON en un diccionario

# Función para crear cabeceras
def crear_cabecera():
    return {
        'Authorization': 'Bearer '+env("ACCESS_TOKEN"),
        "Content-Type": "application/json"
}
        

def obtener_datos_api():
    # Paso 1: Obtener la versión de la API desde el archivo .env (por ejemplo, 'v1' o 'v2')
    api_version = env("API_VERSION")  # Esto podría ser 'v1' o 'v2'
    
    # Paso 2: Cargar los formatos de respuesta desde el archivo .env (JSON o XML)
    api_formatos = json.loads(env('API_FORMATOS'))  # Carga el diccionario {'v1': 'json', 'v2': 'xml'}
    
    # Paso 3: Determinar el formato de respuesta basado en la versión de la API
    formato = api_formatos.get(api_version, 'json')  # Por defecto usamos 'json' si no se encuentra la versión
    
    # Paso 4: Crear las cabeceras para la petición (incluye el token de acceso)
    headers = crear_cabecera()
    
    # Paso 5: Construir la URL de la API basada en la versión seleccionada
    url = f'http://127.0.0.1:8000/api/{api_version}/procesadores'  # Ejemplo: 'http://127.0.0.1:8000/api/v1/procesadores'
    
    # Paso 6: Realizar la petición GET a la API
    if formato == 'xml':
        # Si la respuesta es XML, realizamos la petición sin procesarla aún
        response = requests.get(url, headers=headers)
        
        # Aquí podrías hacer algo con XML, como usar un parser (ej. xml.etree.ElementTree)
        # Sin embargo, por simplicidad, este ejemplo solo muestra la estructura para JSON
    else:
        # Si la respuesta es JSON, procesamos la respuesta normalmente
        response = requests.get(url, headers=headers)
        # Convertimos la respuesta a JSON
        data = response.json()  # Si es JSON, lo convertimos a un diccionario Python
    
    # Paso 7: Devolver los datos obtenidos
    return data  # Devuelve los datos, ya sean JSON o procesados en el formato adecuado

# Página principal
def inicio(request):
    return render(request, 'home/index.html')

# Listado de procesadores
def procesadores_lista_api(request):
    headers = crear_cabecera()
    url = f"{api_base_url}{version}/procesadores"
    response = requests.get(url, headers=headers)
    procesadores = response.json()
    return render(request, 'template-api/procesador_list.html', {"procesadores_mostrar": procesadores})

# Versión mejorada de procesadores
def procesadores_lista_mejorada_api(request):
    headers = crear_cabecera()
    url = f"{api_base_url}{version}/procesadores-mejorados"
    response = requests.get(url, headers=headers)
    procesadores = response.json()
    return render(request, 'template-api/procesador_list_mejorado.html', {"procesadores_mostrar": procesadores})

# Listado de gráficas
def graficas_lista_api(request):
    headers = crear_cabecera()
    url = f"{api_base_url}{version}/graficas"
    response = requests.get(url, headers=headers)
    graficas = response.json()
    return render(request, 'template-api/grafica_list.html', {"graficas_mostrar": graficas})

# Listado de fuentes
def fuentes_lista_api(request):
    headers = crear_cabecera()
    url = f"{api_base_url}{version}/fuentes"
    response = requests.get(url, headers=headers)
    fuentes = response.json()
    return render(request, 'template-api/fuente_list.html', {"fuentes_mostrar": fuentes})

# Listado de RAMs
def rams_lista_api(request):
    headers = crear_cabecera()
    url = f"{api_base_url}{version}/rams"
    response = requests.get(url, headers=headers)
    rams = response.json()
    return render(request, 'template-api/ram_list.html', {"rams_mostrar": rams})


#===========================================================================================================================================

#BUSQUEDAS DE AQUI HACIA ABAJO


# Búsqueda simple de procesadores
# Búsqueda simple de procesadores
def procesador_busqueda_simple(request):
    headers = crear_cabecera()
    formulario = BusquedaSimpleProcesador(request.GET)
    
    if not formulario.is_valid():
        return redirect('inicio')

    texto_busqueda = formulario.cleaned_data.get("textoBusqueda")

    url = f"{api_base_url}{version}/procesador_busqueda"
    response = requests.get(url, headers=headers, params={'textoBusqueda': texto_busqueda})

    if response.status_code == 200:
        procesadores = response.json()
        return render(request, 'template-api/procesador_busqueda.html', {"procesadores": procesadores})
    else:
        return render(request, 'errores/404.html', {"message": "No se encontraron procesadores."})

# Búsqueda avanzada de procesadores
def procesador_busqueda_avanzada(request):
    headers = crear_cabecera()
    formulario = BusquedaAvanzadaProcesador(request.GET)
    
    if not formulario.is_valid():
        return redirect('inicio')

    # Recoger los filtros de búsqueda
    nombre = formulario.cleaned_data.get("nombre")
    familia = formulario.cleaned_data.get("familiaprocesador")
    nucleos = formulario.cleaned_data.get("nucleos")
    hilos = formulario.cleaned_data.get("hilos")
    potencia_calculo = formulario.cleaned_data.get("potenciacalculo")

    url = f"{api_base_url}{version}/procesador_busqueda_avanzada"
    response = requests.get(
        url,
        headers=headers,
        params={
            'nombre': nombre,
            'familiaprocesador': familia,
            'nucleos': nucleos,
            'hilos': hilos,
            'potenciacalculo': potencia_calculo
        }
    )

    if response.status_code == 200:
        procesadores = response.json()
        return render(request, 'template-api/procesador_busqueda_avanzada.html', {"procesadores": procesadores})
    else:
        return render(request, 'errores/404.html', {"message": "No se encontraron procesadores."})


#===============================================================================================================================================================
# Vista para la búsqueda avanzada de gráficas
def grafica_busqueda_avanzada(request):
    headers = crear_cabecera()
    formulario = BusquedaAvanzadaGrafica(request.GET)
    
    if not formulario.is_valid():
        return redirect('inicio')

    # Recoger los filtros de búsqueda
    nombre = formulario.cleaned_data.get("nombre")
    familiagrafica = formulario.cleaned_data.get("familiagrafica")
    potenciacalculo = formulario.cleaned_data.get("potenciacalculo")

    url = f"{api_base_url}{version}/grafica_busqueda_avanzada"
    
    try:
        # Realizamos la petición a la API
        response = requests.get(
            url,
            headers=headers,
            params={
                'nombre': nombre,
                'familiagrafica': familiagrafica,
                'potenciacalculo': potenciacalculo
            }
        )

        # Si la respuesta es exitosa (código 200), mostramos las gráficas
        if response.status_code == 200:
            graficas = response.json()
            return render(request, 'template-api/grafica_busqueda_avanzada.html', {"graficas": graficas})
        
        # Si no es 200, utilizamos la función manejar_errores para manejar el error
        return manejar_errores(request, response, formulario, 'template-api/grafica_busqueda_avanzada.html')

    except Exception as err:
        # Capturamos cualquier otro tipo de error inesperado
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)


    
    
#===============================================================================================================================================================
# Vista para la búsqueda avanzada de fuentes
def fuente_busqueda_avanzada(request):
    headers = crear_cabecera()
    formulario = BusquedaAvanzadaFuente(request.GET)
    
    if not formulario.is_valid():
        return redirect('inicio')

    # Recoger los filtros de búsqueda
    vatios = formulario.cleaned_data.get("vatios")
    calidadfuente = formulario.cleaned_data.get("calidadfuente")
    amperaje = formulario.cleaned_data.get("amperaje")

    url = f"{api_base_url}{version}/fuente_busqueda_avanzada"
    response = requests.get(
        url,
        headers=headers,
        params={
            'vatios': vatios,
            'calidadfuente': calidadfuente,
            'amperaje': amperaje
        }
    )

    if response.status_code == 200:
        fuentes = response.json()
        return render(request, 'template-api/fuente_busqueda_avanzada.html', {"fuentes": fuentes})
    else:
        return render(request, 'errores/404.html', {"message": "No se encontraron fuentes."})


#===============================================================================================================================================================
# Vista para la búsqueda avanzada de RAMs
def ram_busqueda_avanzada(request):
    headers = crear_cabecera()
    formulario = BusquedaAvanzadaRam(request.GET)
    
    if not formulario.is_valid():
        return redirect('inicio')

    # Recoger los filtros de búsqueda
    mhz = formulario.cleaned_data.get("mhz")
    familiaram = formulario.cleaned_data.get("familiaram")
    rgb = formulario.cleaned_data.get("rgb")

    url = f"{api_base_url}{version}/ram_busqueda_avanzada"
    response = requests.get(
        url,
        headers=headers,
        params={
            'mhz': mhz,
            'familiaram': familiaram,
            'rgb': rgb
        }
    )

    if response.status_code == 200:
        rams = response.json()
        return render(request, 'template-api/ram_busqueda_avanzada.html', {"rams": rams})
    else:
        return render(request, 'errores/404.html', {"message": "No se encontraron RAMs."})
    
    
#===============================================================================================================================================================
    
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

