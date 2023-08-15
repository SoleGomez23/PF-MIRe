from django import forms
from .models import Metrica
from django.forms import Textarea

class MetricaForm(forms.ModelForm):
    class Meta:
        model = Metrica
        fields = '__all__' 
        widgets = {
            'descripcion': Textarea(attrs={'cols': 30, 'rows': 1}),
   }  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})

class MetricaFormEditar(forms.ModelForm):
    class Meta:
        model = Metrica
        fields = ['descripcion']
        
       