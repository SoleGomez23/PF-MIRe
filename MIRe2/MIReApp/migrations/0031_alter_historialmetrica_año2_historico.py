# Generated by Django 3.2.20 on 2023-10-03 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIReApp', '0030_auto_20231003_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialmetrica',
            name='año2_historico',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
