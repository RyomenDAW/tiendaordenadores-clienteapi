from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
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


#======================================================================================================================================================

