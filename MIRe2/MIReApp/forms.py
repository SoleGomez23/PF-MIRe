from django import forms 
from .models import Metrica

class MetricaForm(forms.ModelForm):
    class Meta:
        model = Metrica
        fields = '__all__'