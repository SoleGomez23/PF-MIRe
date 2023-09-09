from django import forms 
from .models import Metrica, Indicador, Tipo

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
        
        self.fields['tipo'].queryset = Tipo.objects.none()
        if 'ambito' in self.data:
            try:
                ambito_id = int(self.data.get('ambito'))
                self.fields['tipo'].queryset = Tipo.objects.filter(ambito_id=ambito_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Tipo queryset
        elif self.instance.pk:
            self.fields['tipo'].queryset = self.instance.ambito.tipo_set.order_by('nombre')

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
        fields = ['descripcion', 'ambito','tipo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
            
        self.fields['tipo'].queryset = Tipo.objects.none()
        if 'ambito' in self.data:
            try:
                ambito_id = int(self.data.get('ambito'))
                self.fields['tipo'].queryset = Tipo.objects.filter(ambito_id=ambito_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Tipo queryset
        elif self.instance.pk:
            self.fields['tipo'].queryset = self.instance.ambito.tipo_set.order_by('nombre')

class IndicadorFormVer(forms.ModelForm):
    class Meta:
        model = Indicador
        fields = ['descripcion','ambito','tipo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
        
       