from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from .helper import helper

#================================================================================================================================

class BusquedaAvanzadaProcesador(forms.Form):
    FAMILIA_PROCESADOR = (
        ("Ryzen", "Ryzen"),
        ("Intel", "Intel"),
    )

    nombre = forms.CharField(
        required=False,
        label="Nombre del Procesador",
        max_length=100,
    )
    familiaprocesador = forms.ChoiceField(
        required=False,
        label="Familia del Procesador",
        choices=[('', 'Seleccione una familia')] + list(FAMILIA_PROCESADOR),
    )
    potencia_min = forms.IntegerField(
        required=False,
        label="Potencia de Cálculo Mínima",
        min_value=0,
    )
    potencia_max = forms.IntegerField(
        required=False,
        label="Potencia de Cálculo Máxima",
        min_value=0,
    )
    nucleos = forms.IntegerField(
        required=False,
        label="Número de Núcleos",
        min_value=1,
    )
    hilos = forms.IntegerField(
        required=False,
        label="Número de Hilos",
        min_value=1,
    )
    urlcompra = forms.URLField(
        required=False,
        label="URL de Compra",
        max_length=100,
    )

    
#Retorna en 2 diferentes porque si no me daba un error raro.


class BusquedaSimpleProcesador(forms.Form):
    textoBusqueda = forms.CharField(
        required=False,
        label="Nombre del Procesador",
        max_length=100,
    )
    
    
#======================================================================================================================================================

class BusquedaAvanzadaGrafica(forms.Form):
    FAMILIA_GRAFICA = (
        ("", "Seleccione una familia"),
        ("NVIDIA", "NVIDIA"),
        ("AMD", "AMD"),
        ("Intel", "Intel")

        # Añade más familias de gráficas si es necesario
    )
    
    nombre = forms.CharField(
        required=False,
        label="Nombre de la Gráfica",
        max_length=100,
    )
    familiagrafica = forms.ChoiceField(
        required=False,
        label="Familia de la Gráfica",
        choices=FAMILIA_GRAFICA,
    )

    potenciacalculo = forms.IntegerField(
        required=False,
        label="Potencia de Cálculo",
        min_value=0,
    )
    memoriavram = forms.IntegerField(
        required=False,
        label="Memoria VRAM ",
        min_value=0,
    )
    trazadorayos = forms.BooleanField(
        required=False,
        label="Con Trazador de Rayos",
        initial=False,
    )
    urlcompra = forms.URLField(
        required=False,
        label="URL de Compra",
        max_length=100,
    )
    
 #======================================================================================================================================================   

class BusquedaAvanzadaFuente(forms.Form):
    SELLO_CALIDAD_FUENTE = (
        ("80Bronce", "80Bronce"),
        ("80Silver", "80Silver"),
        ("80Gold", "80Gold"),
        ("80Plat", "80Plat"),
        ("80Titanium", "80Titanium"),
    )

    vatios = forms.IntegerField(
        required=False,
        label="Vatios Mínimos",
        min_value=0,
    )

    amperaje = forms.FloatField(
        required=False,
        label="Amperaje Mínimo",
        min_value=0,
    )

    calidadfuente = forms.ChoiceField(
        required=False,
        label="Calidad de la Fuente",
        choices=SELLO_CALIDAD_FUENTE,
    )
    
    urlcompra = forms.URLField(
        required=False,
        label="URL de Compra",
        max_length=100,
    )





#======================================================================================================================================================

class BusquedaAvanzadaRam(forms.Form):
    FAMILIA_RAM = (
        ("DDR3", "Formato DDR3"),
        ("DDR4", "Formato DDR4"),
        ("DDR5","Formato DDR5"),
    )
    
    mhz = forms.CharField(
        required=False,
        label="Frecuencia Mínima (MHz)",
    )

    familiaram = forms.CharField(
        required=False,
        label="Familia de RAM",
    )
    rgb = forms.BooleanField(
        required=False,
        label="Con RGB",
        initial=False,
    )
    
    urlcompra = forms.URLField(
        required=False,
        label="URL de Compra",
        max_length=100,
    )

#======================================================================================================================================================


class ProcesadorForm(forms.Form):
    FAMILIA_PROCESADOR = (
    ("Ryzen", "Ryzen"),
    ("Intel", "Intel"),
    )
    
    
    nombre = forms.CharField (label="Nombre del procesador",
                              required=True, max_length=100,
                              help_text="100 caracteres como maximo")
    
    urlcompra = forms.URLField(label="URL de compra",
                               required=True, max_length=100,
                               help_text="100 caracteres como maximo")
    
    familiaprocesador = forms.ChoiceField(
        label="Familia del procesador",
        choices=FAMILIA_PROCESADOR,
        required=True
    )
    
    potenciacalculo = forms.IntegerField (label="Potencia del procesador",
                              required=True,
                              help_text="50 cifras como maximo")
    
    nucleos = forms.IntegerField (label="Nucleos del procesador",
                              required=True,
                              help_text="50 cifras como maximo")
    
    hilos = forms.IntegerField (label="Hilos del procesador",
                              required=True,
                              help_text="50 cifras como maximo")
    
    imagen = forms.ImageField(label = "Imagen del procesador",required=False)    
    
    

class ProcesadorActualizarNombreForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, label="Nuevo Nombre para procesador colega")





FAMILIA_GRAFICA = (
    ("AMD", "AMD"),
    ("Nvidia", "NVIDIA"),
    ("Intel", "Intel")
)

class GraficaForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre de la Gráfica!",
        required=True,
        max_length=100,
        help_text="100 caracteres como máximo"
    )

    urlcompra = forms.URLField(
        label="URL de compra",
        required=True,
        max_length=100,
        help_text="100 caracteres como máximo"
    )

    familiagrafica = forms.ChoiceField(
        label="Familia de la Gráfica",
        choices=FAMILIA_GRAFICA,
        required=True
    )

    potenciacalculo = forms.IntegerField(
        label="Potencia de Cálculo",
        required=True,
        help_text="Ingrese un valor positivo"
    )

    memoriavram = forms.IntegerField(
        label="Memoria VRAM (GB)",
        required=True,
        help_text="Ingrese la cantidad de memoria VRAM en GB"
    )

    trazadorayos = forms.BooleanField(
        label="¿Tiene Trazado de Rayos?",
        required=False
    )

    grafica_procesadores = forms.IntegerField(
        label="ID del Procesador",
        required=True,
        help_text="Seleccione un procesador relacionado con la gráfica"
    )


class ActualizarNombreGraficaForm(forms.Form):
    nombre = forms.CharField(
        label="Nuevo Nombre de la Gráfica",
        required=True,
        max_length=100,
        help_text="Máximo 100 caracteres."
    )
    
    
from django import forms

from django import forms

class MonitorGraficaForm(forms.Form):
    """ Formulario para la relación ManyToMany entre Monitor y Grafica """

    monitor = forms.IntegerField(
        label="ID del Monitor",
        required=True,
        min_value=1,
        help_text="Selecciona un Monitor válido (ID numérico)."
    )

    grafica = forms.IntegerField(
        label="ID de la Gráfica",
        required=True,
        min_value=1,
        help_text="Selecciona una Tarjeta Gráfica válida (ID numérico)."
    )

    modo_conexion = forms.ChoiceField(
        choices=[("HDMI", "HDMI"), ("DisplayPort", "DisplayPort"), ("VGA", "VGA"), ("DVI", "DVI")],
        label="Modo de Conexión",
        required=True
    )

    es_monitor_gaming = forms.BooleanField(
        label="¿Es un Monitor Gaming?",
        required=False
    )

    resolucion_maxima = forms.IntegerField(
        label="Resolución Máxima (píxeles)",
        required=True,
        min_value=720,
        max_value=4320
    )

    def clean(self):
        """ Validaciones personalizadas """
        cleaned_data = super().clean()
        monitor = cleaned_data.get("monitor")
        grafica = cleaned_data.get("grafica")

        if monitor == grafica:
            raise forms.ValidationError("❌ ¡El mismo dispositivo no puede conectarse a sí mismo!")

        return cleaned_data


    # class Procesador (models.Model):
    # id_procesador = models.AutoField(primary_key=True)
    # urlcompra = models.URLField(max_length=100)
    # nombre = models.TextField(max_length=100)
    # familiaprocesador = models.TextField(max_length=6, choices=FAMILIA_PROCESADOR)
    # potenciacalculo = models.PositiveBigIntegerField()
    # nucleos = models.PositiveSmallIntegerField()
    # hilos = models.PositiveIntegerField(validators=[MinValueValidator(35000)])  # Este validator luego se suprime por el form y view xd
    # imagen = models.ImageField(upload_to='procesadores/', blank=True, null=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Aquí usamos CustomUser en lugar de User

    # # Relación OneToOne con PlacaBase
    # placabase = models.OneToOneField('PlacaBase', on_delete=models.CASCADE, null=True, blank=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Aquí usamos CustomUser en lugar de User   
    