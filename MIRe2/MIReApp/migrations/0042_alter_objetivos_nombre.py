# Generated by Django 3.2.20 on 2023-10-27 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIReApp', '0041_alter_programa_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objetivos',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]