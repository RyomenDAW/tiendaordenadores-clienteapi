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



    Llamar siempre a la variable de entorno y a las claves desde un único método.



    Otorgar Permisos a las Vistas, y crear tokens específicos para esos usuarios y permisos



========================================================================================================================================================
Crear una variable de entorno, y añadir una clave para cada tipo de usuario que tengais en vuestra base de datos. Añadirlos en la variable de entorno. (Esta variable la tenéis que quitar del .gitignore, no es seguro, pero al estar en un entorno de aprendizaje, lo haremos asi)(1 punto)


========================================================================================================================================================
Crear dos consultas mejorada a un listado de otro modelo de vuestra aplicación. (1.5 punto)



========================================================================================================================================================
Incluir otro tipo de autenticación a vuestra aplicación por API e incluir una consulta mejorada a oto modelo que no se haya realizado antes. Explicar como se configura mediante un documento o presentacion(2.5 punto)

    Esto va en la presentacion que te he adjuntado previamente.