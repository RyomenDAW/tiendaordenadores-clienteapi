from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
from requests.exceptions import HTTPError

import requests
import environ
import os
from pathlib import Path

from django.http import JsonResponse

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
        'Authorization': 'Token ' + env("ACCESS_TOKEN"),  # 🔹 Usa "Token" en lugar de "Bearer"
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
    url = f'http://127.0.0.1:8000/{api_version}/procesadores'  # Ejemplo: 'http://127.0.0.1:8000/api/v1/procesadores'
    
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
    url = f"{api_base_url}template-api/procesadores"
    response = requests.get(url, headers=headers)
    procesadores = response.json()
    return render(request, 'template-api/procesador_list.html', {"procesadores_mostrar": procesadores})

def placasbase_lista_api(request):
   headers = crear_cabecera()
   url = f"{api_base_url}{version}/placasbase"
   response = requests.get(url, headers=headers)
   placasbase = response.json()
   return render(request, 'template-api/placasbase_list.html', {"placasbase_mostrar": placasbase})


def procesadores_lista_mejorada_api(request):
    headers = crear_cabecera()
    url = f"{api_base_url}{version}/procesadores-mejorados"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 🚨 Esto lanza un error si la API devuelve 404 o 500

        print("🔎 Respuesta de la API:", response.text)  # 🔥 DEPURACIÓN: Mira qué está devolviendo la API

        procesadores = response.json()  # 👈 Aquí puede estar fallando

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Error HTTP al obtener procesadores: {http_err}")
        return render(request, 'errores/500.html', {"error": f"Error HTTP: {http_err}"})

    except requests.exceptions.JSONDecodeError:
        print("❌ La API no devolvió un JSON válido")
        return render(request, 'errores/500.html', {"error": "La API no devolvió un JSON válido"})

    except requests.exceptions.RequestException as req_err:
        print(f"❌ Error de conexión con la API: {req_err}")
        return render(request, 'errores/500.html', {"error": "Error de conexión con la API"})

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
    
   # Vista para manejar el formulario y hacer un POST a la API (Crear Procesador)
def crear_procesador(request):
    if request.method == "POST":
        form = ProcesadorForm(request.POST, request.FILES)

        if form.is_valid():
            headers = crear_cabecera()

            data = {
                "nombre": form.cleaned_data["nombre"],
                "urlcompra": form.cleaned_data["urlcompra"],
                "familiaprocesador": form.cleaned_data["familiaprocesador"],
                "potenciacalculo": form.cleaned_data["potenciacalculo"],
                "nucleos": form.cleaned_data["nucleos"],
                "hilos": form.cleaned_data["hilos"]
            }

            response = requests.post(
                "http://127.0.0.1:8000/template-api/procesadores/",
                json=data,
                headers=headers
            )

            if response.status_code == 201:
                messages.success(request, "✅ Procesador creado correctamente.")
                return redirect("procesadores_lista_api")
            else:
                error_message = f"Error {response.status_code}: {response.text}"
                form.add_error(None, error_message)

    else:
        form = ProcesadorForm()

    return render(request, 'procesadores/crear_procesador.html', {'form': form})


# Vista para Editar un Procesador
def editar_procesador(request, procesador_id):
    procesador_data = helper.obtener_procesador(procesador_id)

    if not procesador_data:
        messages.error(request, "❌ No se encontró el procesador.")
        return redirect("procesadores_lista_api")

    if request.method == "POST":
        form = ProcesadorForm(request.POST, request.FILES)

        if form.is_valid():
            datos = {
                "nombre": form.cleaned_data["nombre"],
                "urlcompra": form.cleaned_data["urlcompra"],
                "familiaprocesador": form.cleaned_data["familiaprocesador"],
                "potenciacalculo": form.cleaned_data["potenciacalculo"],
                "nucleos": form.cleaned_data["nucleos"],
                "hilos": form.cleaned_data["hilos"]
            }

            result = helper.api_request("put", f"{procesador_id}/", data=datos)

            if result:
                messages.success(request, "✅ Procesador actualizado correctamente.")
                return redirect("procesadores_lista_api")
            else:
                form.add_error(None, "❌ Error al actualizar el procesador.")

    else:
        form = ProcesadorForm(initial=procesador_data)

    return render(request, "procesadores/actualizar.html", {"formulario": form})


# Vista para actualizar solo el nombre de un procesador
def actualizar_nombre_procesador(request, procesador_id):
    procesador_data = helper.obtener_procesador(procesador_id)

    if not procesador_data:
        messages.error(request, "❌ No se encontró el procesador.")
        return redirect("procesadores_lista_api")

    if request.method == "POST":
        form = ProcesadorActualizarNombreForm(request.POST)

        if form.is_valid():
            nuevo_nombre = form.cleaned_data["nombre"]

            resultado = helper.actualizar_nombre_procesador(procesador_id, nuevo_nombre)

            if resultado:
                messages.success(request, "✅ Nombre del procesador actualizado correctamente.")
                return redirect("procesadores_lista_api")
            else:
                form.add_error(None, "❌ Error al actualizar el nombre del procesador.")

    else:
        form = ProcesadorActualizarNombreForm(initial={"nombre": procesador_data["nombre"]})

    return render(request, "procesadores/actualizar_nombre.html", {"formulario": form})


# Vista para eliminar un procesador
def eliminar_procesador(request, procesador_id):
    resultado = helper.eliminar_procesador(procesador_id)

    if resultado is not None:
        messages.success(request, "✅ Procesador eliminado correctamente.")
    else:
        messages.error(request, "❌ Error al eliminar el procesador.")

    return redirect("procesadores_lista_api")



def crear_grafica_cliente(request):
    if request.method == "POST":
        form = GraficaForm(request.POST)

        if form.is_valid():
            headers = crear_cabecera()

            datos = {
                "nombre": form.cleaned_data["nombre"],
                "urlcompra": form.cleaned_data["urlcompra"],
                "familiagrafica": form.cleaned_data["familiagrafica"],
                "potenciacalculo": form.cleaned_data["potenciacalculo"],
                "memoriavram": form.cleaned_data["memoriavram"],
                "trazadorayos": form.cleaned_data["trazadorayos"],
                "grafica_procesadores": form.cleaned_data["grafica_procesadores"],  # Procesador asociado
                "user": request.user.id  # 🔥 Asegurar que el usuario autenticado se pase
            }

            print("📡 Enviando datos:", datos)  # Debug para verificar lo que se envía

            response = requests.post(
                "http://127.0.0.1:8000/template-api/graficas/",
                json=datos,
                headers=headers
            )

            print("🔎 API Response:", response.status_code, response.text)  # Debug

            if response.status_code == 201:
                messages.success(request, "✅ ¡Gráfica creada con éxito!")  # ✅ Mensaje de éxito
                return redirect("graficas_lista_api")  # Redirigir tras crear la gráfica
            else:
                form.add_error(None, f"❌ Error en API: {response.text}")

    else:
        form = GraficaForm()

    return render(request, 'graficas/crear_grafica.html', {'form': form})



def editar_grafica_cliente(request, grafica_id):
    """ Editar una gráfica desde el cliente """

    # Obtener datos actuales de la gráfica desde la API
    grafica_data = helper.obtener_grafica(grafica_id)

    if not grafica_data:
        messages.error(request, "❌ No se encontró la gráfica.")
        return redirect("graficas_lista_api")

    if request.method == "POST":
        form = GraficaForm(request.POST)

        if form.is_valid():
            headers = crear_cabecera()

            datos = {
                "nombre": form.cleaned_data["nombre"],
                "urlcompra": form.cleaned_data["urlcompra"],
                "familiagrafica": form.cleaned_data["familiagrafica"],
                "potenciacalculo": form.cleaned_data["potenciacalculo"],
                "memoriavram": form.cleaned_data["memoriavram"],
                "trazadorayos": form.cleaned_data["trazadorayos"],
                "grafica_procesadores": form.cleaned_data["grafica_procesadores"],  # Procesador asociado
                "user": request.user.id if request.user.is_authenticated else None
            }

            response = requests.put(
                f"http://127.0.0.1:8000/template-api/graficas/{grafica_id}/",
                json=datos,
                headers=headers
            )

            if response.status_code == 200:
                messages.success(request, "✅ Gráfica actualizada correctamente.")
                return redirect("graficas_lista_api")  # Redirigir tras actualizar
            else:
                form.add_error(None, f"❌ Error en API: {response.text}")

    else:
        form = GraficaForm(initial=grafica_data)  # Prellenar formulario con los datos actuales

    return render(request, "graficas/actualizar.html", {"formulario": form})


def actualizar_nombre_grafica_cliente(request, grafica_id):
    """ Vista cliente para actualizar solo el nombre de la gráfica """

    if request.method == "POST":
        form = ActualizarNombreGraficaForm(request.POST)

        if form.is_valid():
            nuevo_nombre = form.cleaned_data["nombre"]
            resultado = helper.actualizar_nombre_grafica(grafica_id, nuevo_nombre)

            if resultado:
                messages.success(request, "✅ Nombre de la gráfica actualizado correctamente.")
                return redirect("graficas_lista_api")  # Redirigir tras actualizar
            else:
                form.add_error(None, "❌ Error al actualizar el nombre de la gráfica.")

    else:
        form = ActualizarNombreGraficaForm()

    return render(request, "graficas/actualizar_nombre.html", {"formulario": form})


def eliminar_grafica(request, grafica_id):
    """ Elimina una gráfica a través de la API """
    resultado = helper.eliminar_grafica(grafica_id)

    if resultado is not None:
        messages.success(request, "✅ La gráfica se eliminó correctamente.")
    else:
        messages.error(request, "❌ No se pudo eliminar la gráfica.")

    return redirect("graficas_lista_api")  # Redirige a la lista de gráficas después de eliminar
#==========================================================================================================================

# 📌 CREAR RELACIÓN Monitor-Grafica (POST)
def crear_monitor_grafica_cliente(request):
    if request.method == "POST":
        form = MonitorGraficaForm(request.POST)

        if form.is_valid():
            data = {
                "monitor": form.cleaned_data["monitor"],
                "grafica": form.cleaned_data["grafica"],
                "modo_conexion": form.cleaned_data["modo_conexion"],
                "es_monitor_gaming": form.cleaned_data["es_monitor_gaming"],
                "resolucion_maxima": form.cleaned_data["resolucion_maxima"]
            }

            response = helper.api_request("post", "crear/", data, tipo="monitores-graficas")

            if response:
                messages.success(request, "✅ ¡Relación Monitor-Grafica creada con éxito!")
                return redirect("graficas_lista_api")
            else:
                messages.error(request, "❌ Error al crear la relación Monitor-Grafica.")

    else:
        form = MonitorGraficaForm()

    return render(request, "monitores-graficas/crear.html", {"formulario": form})


# 📌 ACTUALIZAR RELACIÓN Monitor-Grafica (PUT)
def actualizar_monitor_grafica_cliente(request, relacion_id):
    relacion = helper.api_request("get", f"{relacion_id}/", tipo="monitores-graficas")  # 🔥 FIX

    if not relacion:
        messages.error(request, "❌ No se encontró la relación Monitor-Grafica.")
        return redirect("graficas_lista_api")

    if request.method == "POST":
        form = MonitorGraficaForm(request.POST)

        if form.is_valid():
            data = {
                "monitor": form.cleaned_data["monitor"],
                "grafica": form.cleaned_data["grafica"],
                "modo_conexion": form.cleaned_data["modo_conexion"],
            }

            response = helper.api_request("put", f"{relacion_id}/", data, tipo="monitores-graficas")  # 🔥 FIX

            if response:
                messages.success(request, "✅ ¡Relación Monitor-Grafica actualizada con éxito!")
                return redirect("graficas_lista_api")
            else:
                messages.error(request, "❌ Error al actualizar la relación Monitor-Grafica.")

    else:
        form = MonitorGraficaForm(initial=relacion)

    return render(request, "monitores-graficas/actualizar.html", {"formulario": form})


# 📌 ACTUALIZAR SOLO LA GRÁFICA EN LA RELACIÓN (PATCH)
def actualizar_grafica_en_relacion_cliente(request, relacion_id):
    """ Vista para actualizar solo la gráfica en una relación Monitor-Grafica """
    
    relacion = helper.api_request("get", f"{relacion_id}/", tipo="monitores-graficas")

    if not relacion:
        messages.error(request, "❌ No se encontró la relación Monitor-Grafica.")
        return redirect("graficas_lista_api")

    if request.method == "POST":
        nueva_grafica = request.POST.get("grafica")

        if not nueva_grafica:
            messages.error(request, "❌ Debes seleccionar una gráfica.")
        else:
            response = helper.api_request("patch", f"{relacion_id}/actualizar-grafica/", 
                                          data={"grafica": nueva_grafica}, tipo="monitores-graficas")
            
            if response:
                messages.success(request, "✅ ¡Gráfica actualizada correctamente en la relación!")
                return redirect("graficas_lista_api")
            else:
                messages.error(request, "❌ Error al actualizar la gráfica en la relación.")

    return render(request, "monitores-graficas/actualizar-grafica.html", {"relacion": relacion})


# 📌 ELIMINAR RELACIÓN Monitor-Grafica (DELETE)
def eliminar_monitor_grafica_cliente(request, relacion_id):
    response = helper.api_request("delete", f"{relacion_id}/", tipo="monitores-graficas")  # 🔥 FIX

    if response:
        messages.success(request, "✅ ¡Relación Monitor-Grafica eliminada correctamente!")
    else:
        messages.error(request, "❌ Error al eliminar la relación Monitor-Grafica.")

    return redirect("graficas_lista_api")


#=============================================================================================================

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

