from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models
 
FRECUENCIAS = (
    ('Bianual','Bianual'),
    ('Anual', 'Anual'),
    ('Semestral','Semestral'),
    ('Mensual','Mensual')
)

AMBITOS = (
    ('Fin','Fin'),
    ('Propósito','Propósito'),
    ('Componente','Componente'),
    ('Actividades','Actividades'),
)
TIPOS = (
    ('Eficiencia','Eficiencia'),
    ('Eficacia','Eficacia'),
    ('Economía','Economía'),
    ('Calidad','Calidad')
)
# Create your models here.
class Metrica(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, 
                              verbose_name='Título',
                              unique= True,
                              validators= [
                                  RegexValidator(regex= r'^[a-zA-Z\s]*$',
                                                 message="El nombre no puede contener caracteres especiales.",
                                                 code='invalid_nombre')
                              ])
    descripcion = models.TextField(max_length=100, verbose_name='Descripción', null=True) 
    unidad_medida = models.CharField(max_length=100, 
                                        verbose_name='Unidad de Medida',
                                        validators= [
                                            RegexValidator(regex= r'^[a-zA-Z\s]*$',
                                                            message="La unidad de medida no puede contener caracteres especiales",
                                                            code='invalid_nombre')
                                        ])
    valor = models.IntegerField(verbose_name='Valor', validators=[MinValueValidator(0, message="El valor no puede ser negativo")], default=0)
    frecuencia = models.CharField(max_length=10, choices=FRECUENCIAS)
    year = models.PositiveIntegerField(blank=True, null=True,verbose_name='Ingrese año:')

    def __str__(self):
        fila = 'Título: ' + self.titulo + ' - ' + 'Descripcíon: ' + self.descripcion
        return fila
    
class Indicador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, 
                              verbose_name='Nombre',
                              unique= True,
                              validators= [
                                  RegexValidator(regex= r'^[a-zA-Z\s]*$',
                                                 message="El nombre no puede contener caracteres especiales.",
                                                 code='invalid_nombre')
                              ])
    descripcion = models.TextField(max_length=100, verbose_name='Descripción', null=True) 
    frecuencia = models.CharField(verbose_name='Frecuencia de medición',max_length=10, choices=FRECUENCIAS,default='Anual')
    ambito = models.CharField(verbose_name='¿Qué se está midiendo?',max_length=20, choices=AMBITOS)
    tipo = models.CharField(verbose_name='Tipo',max_length=10, choices=TIPOS)

    def __str__(self):
        fila = 'Nombre: ' + self.titulo + ' - ' + 'Descripcíon: ' + self.descripcion
        return fila
    
class HistorialMetrica(models.Model):
    metrica = models.ForeignKey(Metrica, on_delete=models.CASCADE)
    año_historico = models.PositiveIntegerField()
    valor_historico = models.PositiveIntegerField(default=0)  # Agrega un valor predeterminado

    def __str__(self):
        return f"Métrica: {self.metrica.titulo} - Año Histórico: {self.año_historico} - Valor Histórico: {self.valor_historico}"