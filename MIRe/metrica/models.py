from django.db import models

# Create your models here.
class Metrica(models.Model):
    nombre = models.CharField(max_length=50,primary_key=True, blank = False, null= False),
    perido = models.CharField(max_length = 100),
    uMedida = models.CharField(max_length = 100),