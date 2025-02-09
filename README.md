========================================================================================================================================================

Configurar vuestra aplicación para que tenga una API REST y que sea accesible desde pythonanywhere.Enviar enlace de github(1 punto)

    Enlace pythonanywhere.

    https://ryomendaw.pythonanywhere.com/

    Enlace aplicacion API REST

    https://github.com/RyomenDAW/aplicacionwebparte1

========================================================================================================================================================
Crear una aplicación para que consulte vuestra API REST. Enviarme enlace github. (1 punto)

    https://github.com/RyomenDAW/tiendaordenadores-clienteapi

========================================================================================================================================================


Crear una consulta sencilla al listado de vuestro modelo principal de la aplicación y mostrarla en vuestra aplicación cliente. (1 punto)

    Mi consulta sencilla que lista mi modelo principal, es esta:

    def procesadores_lista_api(request):
        #Obtenemos todos los procesadores
        headers = {'Authorization': 'Bearer sfTTDSS3wekREQ3lAJ5sBcR07JOxVx'}
        response = requests.get('http://127.0.0.1:8000/api/v1/procesadores', headers = headers)
        #Transformamos la respuesta en json
        procesadores = response.json()
        return render(request, 'template-api/procesador_list.html',{"procesadores_mostrar":procesadores})


    Esto lo que hará es consultar al servidor, la lista de procesadores, y devolverá en el cliente la información de estos, ya que es una consulta sencilla, no tendrá atributos de otros de modelos, es decir, aquellos que sean de relaciones.

========================================================================================================================================================

Crear una consulta mejorada al listado de vuestro modelo principal de la aplicación cliente. Debe ser una vista distinta a la anterior, con un template y url disntinta. (1 punto)

Para la consulta mejorada tenemos esto:

class ProcesadorMejoradoSerializer(serializers.ModelSerializer):
    placabase = serializers.PrimaryKeyRelatedField(read_only=True)
    user  = UsuarioSerializer()
    class Meta:
        model = Procesador
        fields = ['id_procesador', 'urlcompra', 'nombre', 'familiaprocesador', 'potenciacalculo','nucleos','hilos','imagen','user','placabase']


Pasamos el campo placabase (relacion) y el campo user (Quien creo ese procesador? )

El template es este: /tiendaordenadores-clienteapi/tiendaordenadores/template-api/procesador_list_mejorado.html

La url es esta:  path('template-api/procesador_list_mejorado.html', views.procesadores_lista_mejorada_api, name='procesadores_lista_mejorada_api')



========================================================================================================================================================
Añadir seguridad en OAUTH 2 a vuestra API REST. (1 punto)

    Como he desarrollado los siguientes diferentes permisos:

    


    Guardar los tokens de acceso en una variable de entorno
.env


    Llamar siempre a la variable de entorno y a las claves desde un único método.



    Otorgar Permisos a las Vistas, y crear tokens específicos para esos usuarios y permisos



========================================================================================================================================================
Crear una variable de entorno, y añadir una clave para cada tipo de usuario que tengais en vuestra base de datos. Añadirlos en la variable de entorno. (Esta variable la tenéis que quitar del .gitignore, no es seguro, pero al estar en un entorno de aprendizaje, lo haremos asi)(1 punto)


.env esta todo, mis 4 roles.

========================================================================================================================================================
Crear dos consultas mejorada a un listado de otro modelo de vuestra aplicación. (1.5 punto)

Grafica y Fuente

class GraficaMejoradaSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer()
    procesador = ProcesadorMejoradoSerializer(source='grafica_procesadores', read_only=True)
    placabase = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Grafica
        fields = ['id_grafica', 'urlcompra', 'nombre', 'familiagrafica', 'potenciacalculo', 
                  'memoriavram', 'fecha_salida', 'trazadorayos', 'user', 'procesador', 'placabase']
        
class FuenteAlimentacionMejoradaSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer()
    class Meta:
        model = FuenteAlimentacion
        fields = ['id_fuente', 'urlcompra', 'vatios', 'amperaje', 
                  'conectoresdisponibles', 'calidadfuente', 'user']


    path('template-api/grafica_list.html', views.graficas_lista_api, name='graficas_lista_api'),
    path('template-api/fuente_list.html', views.fuentes_lista_api, name='fuentes_lista_api'),

========================================================================================================================================================
Incluir otro tipo de autenticación a vuestra aplicación por API e incluir una consulta mejorada a oto modelo que no se haya realizado antes. Explicar como se configura mediante un documento o presentacion(2.5 punto)

    Esto va en el documento adjuntado, llamado securizacion API, de hecho te he puesto 2, ya que jwt creo que lo hara todo el mundo.

El otro modelo sera  RAM.





===================================================================================================================================================================

Por cada petición que hemos hecho, se ha incluido siempre lo siguiente:http://127.0.0.1:8000/api/v1/libros/, que pasaría si en un futuro, la versión cambiar.¿Deberíamos cambiarlo en todos los sitios de la aplicación?¿Cómo podríamos mejorarlo? (1 punto)


Para evitar tener que actualizar la URL de la API manualmente en múltiples lugares, podemos hacer algo similar a lo que hicimos anteriormente con el token Bearer. En lugar de hardcodear la versión en cada solicitud, podríamos almacenar la versión de la API en un archivo .env, lo que nos permitirá configurarlo de manera centralizada.

Implementación:
Archivo .env: Creamos una variable en el archivo .env que almacene la versión de la API. Por ejemplo, la variable API_VERSION=api/v1.


Luego, podemos acceder a esa variable en nuestras vistas (o donde sea necesario) usando un gestor de variables de entorno, como env('API_VERSION').

Petición a la API: En lugar de escribir manualmente la URL completa de la API con la versión, utilizamos la variable que hemos obtenido del archivo .env. Esto hace que, si en el futuro necesitamos cambiar la versión de la API, solo tengamos que modificarla en el archivo .env, y el cambio se reflejará en toda la aplicación.


# Accedemos a la variable 'API_VERSION' desde el archivo settings.py
api_base_url = "http://127.0.0.1:8000/"
version = settings.API_VERSION  # 'api/v1' o la versión que tengamos en el archivo .env


# Construimos la URL completa para hacer la solicitud a la API
url = f"{api_base_url}{version}/fuente_busqueda_avanzada"

Necesitas cambiar la versión de la API?, solo tendrías que modificar el archivo .env y cambiar el valor de API_VERSION, yo he puesto ya el mio en el .env, en mi caso, api/v1.

===================================================================================================================================================================

Para la respuesta siempre incluimos la misma línea:response.json(). ¿Qué pasaría si en el día de mañana cambia el formato en una nueva versión, y en vez de json es xml?¿Debemos volver a cambiar en todos los sitios esa línea? (0,5 puntos)


Añadimos al .env esto

API_FORMATOS='{"v1": "json", "v2": "xml"}'

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


Solo deberiamos de cambiar esa variable .env y añadir eso cuando queramos que sea en los 2 formatos, ahora no tiene mucho sentido ya que no hemos dado XML, pero te he dejado ya esa vista hecha.


===================================================================================================================================================================


¿Siempre debemos tratar todos los errores en cada una de las peticiones?

No, entonces, lo que podemos hacer es centralizar el manejo de los errores en una función que se encargue de esto de manera global, y luego usar esa función en todas nuestras vistas.

Esto tiene varias ventajas:

Evitar duplicar código: Si el manejo de errores es el mismo en todas las peticiones, no tenemos que escribir el mismo código una y otra vez.

Facilitar cambios futuros: Si más adelante necesitamos cambiar cómo tratamos los errores, solo debemos modificar la función centralizada. Esto hace que el código sea más fácil de mantener.


Paso 1: Crear la función de manejo de errores
Primero, creamos una función llamada manejar_errores() que recibirá la respuesta de la API y el formulario. Esta función será responsable de manejar diferentes tipos de errores y devolver la respuesta adecuada.

Aquí te dejo cómo quedaría esta función:

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


Explicación de la función manejar_errores:
========================================================
Chequeo del estado de la respuesta:

Usamos response.raise_for_status() para que si la respuesta tiene un código de error (por ejemplo, 404 o 500), se dispare una excepción. Si la respuesta tiene un código de éxito (200 OK), no pasa nada.


Manejo de errores específicos:

HTTPError: Si la respuesta es un error HTTP, como un 400 (Bad Request), obtenemos el detalle del error desde la respuesta (response.json()) y lo añadimos al formulario.

RequestException: Si no se puede conectar a la API o ocurre un error de red, lanzamos un mensaje de error general.

Exception: Capturamos cualquier otro tipo de error inesperado y lo manejamos de manera genérica.
Devolución de la respuesta:

Si hubo un error 400 (generalmente relacionado con validaciones del servidor), mostramos los errores de validación en el formulario.
Para otros errores, mostramos un error genérico 500 que probablemente redirige a una página de error interna del servidor.

Solamente he modificado esta para que veas:

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



========================================================================================================================================================================

El tutorial de POSTMAN en google docs
    