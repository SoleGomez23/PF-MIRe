from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
class Metrica(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, 
                              verbose_name='Titulo',
                              unique= True,
                              validators= [
                                  RegexValidator(regex= r'^[a-zA-Z\s]*$',
                                                 message="El nombre no puede contener caracteres especiales.",
                                                 code='invalid_nombre')
                              ])
    descripcion = models.TextField(verbose_name='Descripcion', null=True) 
    unidad_medida = models.CharField(max_length=100, 
                                        verbose_name='Unidad de Medida',
                                        unique= True,
                                        validators= [
                                            RegexValidator(regex= r'^[a-zA-Z\s]*$',
                                                            message="La unidad de medida no puede contener caracteres especiales",
                                                            code='invalid_nombre')
                                        ])
    valor = models.IntegerField(verbose_name='Valor', validators=[MinValueValidator(0, message="El valor no puede ser negativo")], default=0)

    def __str__(self):
        fila = 'Titulo: ' + self.titulo + ' - ' + 'Descripcion: ' + self.descripcion
        return fila

#unidad_medida = models.CharField(max_length=100, verbose_name='Unidad de medida')