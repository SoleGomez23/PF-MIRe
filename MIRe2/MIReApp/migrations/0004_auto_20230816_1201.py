# Generated by Django 3.2.20 on 2023-08-16 15:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIReApp', '0003_alter_metrica_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='metrica',
            name='frecuencia',
            field=models.CharField(choices=[('Bianual', 'Bianual'), ('Anual', 'Anual'), ('Semestral', 'Semestral'), ('Mensual', 'Mensual')], default='Anual', max_length=10),
        ),
        migrations.AlterField(
            model_name='metrica',
            name='descripcion',
            field=models.TextField(max_length=100, null=True, verbose_name='Descripcion'),
        ),
        migrations.AlterField(
            model_name='metrica',
            name='titulo',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_nombre', message='El nombre no puede contener caracteres especiales.', regex='^[a-zA-Z\\s]*$')], verbose_name='Titulo'),
        ),
        migrations.AlterField(
            model_name='metrica',
            name='unidad_medida',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_nombre', message='La unidad de medida no puede contener caracteres especiales', regex='^[a-zA-Z\\s]*$')], verbose_name='Unidad de Medida'),
        ),
        migrations.AlterField(
            model_name='metrica',
            name='valor',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='El valor no puede ser negativo')], verbose_name='Valor'),
        ),
    ]