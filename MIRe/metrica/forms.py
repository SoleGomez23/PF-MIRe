from django import forms

class MetricaForm(forms.Form):
    nombre = forms.CharField(label= "Nombre",max_length=50, required=True),
    perido = forms.CharField(label= "Periodo",max_length = 100),
    uMedida = forms.CharField(label= "Unidad de Medida",max_length = 100),
