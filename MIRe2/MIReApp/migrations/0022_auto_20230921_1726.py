# Generated by Django 3.2.20 on 2023-09-21 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIReApp', '0021_auto_20230921_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicador',
            name='denominador_medida',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='indicador',
            name='numerador_medida',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=''),
        ),
    ]