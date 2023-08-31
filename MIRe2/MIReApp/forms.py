from django import forms 
from .models import Metrica
from .models import Indicador

class MetricaForm(forms.ModelForm):
    class Meta:
        model = Metrica
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 10, 'rows': 1}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})

class IndicadorForm(forms.ModelForm):
    class Meta:
        model = Indicador
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})

class MetricaFormEditar(forms.ModelForm):
    class Meta:
        model = Metrica
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 10, 'rows': 3}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})

class IndicadorFormEditar(forms.ModelForm):
    class Meta:
        model = Indicador
        fields = ['descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
        
       