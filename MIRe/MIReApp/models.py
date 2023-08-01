from django.db import models

# Create your models here.
class Metrica(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='Titulo')
    descripcion = models.TextField(verbose_name='Descripcion', null=True) 
    unidad_medida = models.CharField(max_length=100, verbose_name='Unidad de medida')

    def __str__(self):
        fila = 'Titulo: ' + self.titulo + ' - ' + 'Descripcion: ' + self.descripcion
        return fila
