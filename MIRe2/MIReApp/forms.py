from django import forms 
from .models import Metrica, Indicador, Tipo, HistorialMetrica

class MetricaForm(forms.ModelForm):
    class Meta:
        model = Metrica
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 10, 'rows': 1}), #Define las dimensiones del input
            'year2': forms.TextInput(attrs={'readonly': 'readonly'}), #Hace que el campo sea de solo lectura
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'}) #Le agrega la clase form control a todos los campos

class InstanciaForm(forms.ModelForm):
    class Meta:
        model = HistorialMetrica
        fields = '__all__'#widget=forms.TextInput(attrs={'placeholder': 'Año'})    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["año_historico"].widget.attrs.update({'placeholder': 'Ingrese año'})
        self.fields["valor_historico"].widget.attrs.update({'placeholder': 'Ingrese valor'})
        self.fields["valor_historico"].widget.attrs.update({'placeholder': 'Año fin valor'})
        self.fields["año2_historico"].widget.attrs.update({'readonly': 'readonly'})

class IndicadorForm(forms.ModelForm):
    class Meta:
        model = Indicador
        fields = '__all__'       
        widgets = {
            'numerador_medida': forms.TextInput(attrs={'readonly': 'readonly'}),
            'denominador_medida': forms.TextInput(attrs={'readonly': 'readonly'}),
            'numerador_valor': forms.TextInput(attrs={'readonly': 'readonly'}),
            'denominador_valor': forms.TextInput(attrs={'readonly': 'readonly'}),
            'resultado': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})

              
        self.fields['denominador'].queryset = Metrica.objects.none()
        if 'denominador' in self.data:
            try:
                denominador_id = int(self.data.get('denominador'))
                self.fields['denominador'].queryset = Metrica.objects.filter(id=denominador_id).order_by('id')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Tipo queryset
        elif self.instance.pk:
            self.fields['denominador'].queryset = self.instance.denominador.tipo_set.order_by('id')
              
        self.fields['numerador'].queryset = Metrica.objects.none()
        if 'numerador' in self.data:
            try:
                numerador_id = int(self.data.get('numerador'))
                self.fields['numerador'].queryset = Metrica.objects.filter(id=numerador_id).order_by('id')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Tipo queryset
        elif self.instance.pk:
            self.fields['numerador'].queryset = self.instance.numerador.tipo_set.order_by('id')
        
        self.fields['tipo'].queryset = Tipo.objects.none() #Hace el dropdonw de tipo esté vacio al principio
        if 'ambito' in self.data:
            try:
                ambito_id = int(self.data.get('ambito'))
                self.fields['tipo'].queryset = Tipo.objects.filter(ambito_id=ambito_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Tipo queryset
        elif self.instance.pk:
            self.fields['tipo'].queryset = self.instance.ambito.tipo_set.order_by('nombre')

        self.fields['numerador_periodo'].queryset = HistorialMetrica.objects.none()
        if 'numerador_periodo' in self.data:
            try:
                numerador_periodo_id = int(self.data.get('numerador_periodo'))
                self.fields['numerador_periodo'].queryset = HistorialMetrica.objects.filter(id=numerador_periodo_id).order_by('id')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Tipo queryset
        elif self.instance.pk:
            self.fields['numerador_periodo'].queryset = self.instance.numerador_periodo.tipo_set.order_by('id')
                
        self.fields['denominador_periodo'].queryset = HistorialMetrica.objects.none()
        if 'denominador_periodo' in self.data:
            try:
                denominador_periodo_id = int(self.data.get('denominador_periodo'))
                self.fields['denominador_periodo'].queryset = HistorialMetrica.objects.filter(id=denominador_periodo_id).order_by('id')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Tipo queryset
        elif self.instance.pk:
            self.fields['denominador_periodo'].queryset = self.instance.denominador_periodo.tipo_set.order_by('id')

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
        fields = ['descripcion', 'ambito', 'tipo'] #Especifico los campos que voy a mostrar       
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 10, 'rows': 3}),
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


class IndicadorFormVer(forms.ModelForm):
    class Meta:
        model = Indicador
        fields = ['descripcion','ambito','tipo'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
        
       