# Generated by Django 3.2.20 on 2023-09-23 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIReApp', '0025_alter_metrica_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicador',
            name='descripcion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Descripción'),
        ),
    ]