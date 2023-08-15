from django import forms 
from .models import Metrica

class MetricaForm(forms.ModelForm):
    class Meta:
        model = Metrica
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
class MetricaFormEditar(forms.ModelForm):
    class Meta:
        model = Metrica
        fields = ['descripcion']
        
       