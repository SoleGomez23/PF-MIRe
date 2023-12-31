# Generated by Django 3.2.20 on 2023-10-20 20:18

import MIReApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIReApp', '0031_alter_historialmetrica_año2_historico'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=50, null=True)),
                ('objetivo', models.CharField(blank=True, max_length=20, null=True)),
                ('duracion', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='historialmetrica',
            name='mes_historico',
            field=models.CharField(blank=True, choices=[('Enero', 'Enero'), ('Febrero', 'Febrero'), ('Marzo', 'Marzo'), ('Abril', 'Abril'), ('Mayo', 'Mayo'), ('Junio', 'Junio'), ('Julio', 'Julio'), ('Agosto', 'Agosto'), ('Septiembre', 'Septiembre'), ('Octubre', 'Octubre'), ('Noviembre', 'Noviembre'), ('Diciembre', 'Diciembre')], max_length=20, null=True, verbose_name='Ingrese mes:'),
        ),
        migrations.AlterField(
            model_name='historialmetrica',
            name='valor_historico',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='indicador',
            name='formula',
            field=models.CharField(blank=True, choices=[('Inversion promedio', 'Inversion promedio'), ('Tasa de variacion', 'Tasa de variacion'), ('Porcentaje', 'Porcentaje')], max_length=20, verbose_name='Formula'),
        ),
        migrations.AlterField(
            model_name='indicador',
            name='frecuencia',
            field=models.CharField(choices=[('Cuatrienal', 'Cuatrienal'), ('Bianual', 'Bianual'), ('Anual', 'Anual'), ('Semestral', 'Semestral'), ('Mensual', 'Mensual')], max_length=10, verbose_name='Frecuencia de medición'),
        ),
        migrations.AlterField(
            model_name='metrica',
            name='year',
            field=models.PositiveIntegerField(default=None, validators=[MIReApp.models.validate_year], verbose_name='Ingrese año:'),
            preserve_default=False,
        ),
    ]
