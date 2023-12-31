from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

 
FRECUENCIAS = (('Cuatrienal','Cuatrienal'),('Bianual','Bianual'), ('Anual', 'Anual'), ('Semestral','Semestral'), ('Mensual','Mensual'))
FORMULAS = (('Inversion promedio','Inversion promedio'), ('Tasa de variacion','Tasa de variacion'), ('Porcentaje','Porcentaje'))
MESES = (('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),('Diciembre','Diciembre'))
SEMESTRES = (('Enero-Junio', 'Enero-Junio'),('Julio-Diciembre', 'Julio-Diciembre'))
AREAS = (('Ingeniería en Sistemas de Información', 'Ingeniería en Sistemas de Información'),('Ingeniería Química', 'Ingeniería Química'),('Ingeniería Electromecánica', 'Ingeniería Electromecánica'),('Materias Básicas', 'Materias Básicas'))

def validate_year(value):
    current_year = timezone.now().year
    if value < 2010 or value > current_year:
        raise ValidationError(f"El año debe estar en el rango de 2010 a {current_year}.")

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
    descripcion = models.TextField(max_length=100, verbose_name='Descripción', blank=True, null=True)  #blank=True y null=True permiten que el campo se envie vacio 
    unidad_medida = models.CharField(max_length=100, 
                                        verbose_name='Unidad de Medida',
                                        validators= [
                                            RegexValidator(regex= r'^[a-zA-Z\s]*$',
                                                            message="La unidad de medida no puede contener caracteres especiales",
                                                            code='invalid_nombre')
                                        ])
    frecuencia = models.CharField(max_length=10, choices=FRECUENCIAS)
    valor = models.IntegerField(verbose_name='Valor', validators=[MinValueValidator(0, message="El valor no puede ser negativo")], default=0)
    year = models.PositiveIntegerField(verbose_name='Ingrese año:', validators=[validate_year])
    month = models.CharField(max_length=10, verbose_name='Ingrese mes:', choices=MESES, blank=True, null=True)
    semestral = models.CharField(max_length=15, verbose_name='Ingrese semestre:', choices=SEMESTRES, blank=True, null=True,)
    year2 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Segundo año')

    def __str__(self):
        fila = self.titulo
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
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', blank=True, null=True) 
    ambito = models.ForeignKey('Ambito', on_delete=models.CASCADE)
    tipo = models.ForeignKey('Tipo', on_delete=models.CASCADE)
    programa = models.ForeignKey('Programa', on_delete=models.SET_NULL, null=True, blank=True)
    objetivo = models.ForeignKey('Objetivos', on_delete=models.CASCADE, blank=True, null=True)
    frecuencia = models.CharField(verbose_name='Frecuencia de medición',max_length=10, choices=FRECUENCIAS)
    formula = models.CharField(max_length=20, choices= FORMULAS,verbose_name='Formula', blank=True) 
    numerador = models.ForeignKey('Metrica', related_name='Numerador', on_delete=models.CASCADE, blank=True, null=True)
    denominador = models.ForeignKey('Metrica', related_name='Denominador', on_delete=models.CASCADE, blank=True, null=True) 
    numerador_periodo = models.ForeignKey('HistorialMetrica', related_name='Instancia_Numerador', on_delete=models.CASCADE, blank=True, null=True)
    denominador_periodo = models.ForeignKey('HistorialMetrica', related_name='Instancia_Denominador', on_delete=models.CASCADE, blank=True, null=True)
    numerador_medida = models.CharField(max_length=100, verbose_name='', blank=True, null=True) 
    denominador_medida = models.CharField(max_length=100, verbose_name='', blank=True, null=True) 
    numerador_valor = models.PositiveIntegerField(verbose_name='', blank=True, null=True) 
    denominador_valor = models.PositiveIntegerField(verbose_name='' , blank=True, null=True) 
    resultado = models.CharField(max_length=100, verbose_name='', blank=True, null=True)
    estado = models.CharField(max_length=100, verbose_name='Descripción', blank=True, null=True) 

    def __str__(self):
        fila = 'Nombre: ' + self.nombre
        return fila
    
class HistorialMetrica(models.Model):
    id = models.AutoField(primary_key=True)
    metrica = models.ForeignKey(Metrica, on_delete=models.CASCADE)
    año_historico = models.PositiveIntegerField()
    valor_historico = models.PositiveIntegerField()  # Agrega un valor predeterminado
    mes_historico = models.CharField(max_length=20, verbose_name='Ingrese mes:', choices=MESES, blank=True, null=True)
    año2_historico = models.PositiveIntegerField(blank=True, null=True)
    semestre_historico = models.CharField(max_length=15, verbose_name='Ingrese semestre:', choices=SEMESTRES, blank=True, null=True,)

    def __str__(self):
        if self.mes_historico:
            return str(self.año_historico)+ ' - ' + str(self.mes_historico)
        elif self.semestre_historico:
            return str(self.año_historico)+ ' - ' + str(self.semestre_historico)
        elif self.año2_historico:
            return str(self.año_historico)+ ' - ' + str(self.año2_historico)
        else:
            return str(self.año_historico)

class Ambito(models.Model):
    nombre = models.CharField(max_length=15)
    
    def __str__(self):
        return self.nombre
    
class Tipo(models.Model):
    nombre = models.CharField(max_length=15)
    ambito = models.ForeignKey(Ambito, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

    
class Programa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, 
                              verbose_name='Nombre',
                              unique= True,
                              validators= [
                                  RegexValidator(regex= r'^[a-zA-Z\s]*$',
                                                 message="El nombre no puede contener caracteres especiales.",
                                                 code='invalid_nombre')
                              ])
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    objetivo = models.CharField(max_length=100, blank=True, null=True)
    duracion = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre}"

class Objetivos(models.Model):
    id = models.AutoField(primary_key=True)
    programa = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False)
    area = models.CharField(max_length=40, choices=AREAS, blank=True, null=True)
    # frecuencia = models.CharField(max_length=10, choices=FRECUENCIAS)

    # Agrega related_name para evitar el conflicto
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='user',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='user',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username
