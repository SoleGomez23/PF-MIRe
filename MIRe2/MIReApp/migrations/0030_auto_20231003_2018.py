# Generated by Django 3.2.20 on 2023-10-03 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIReApp', '0029_auto_20231003_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialmetrica',
            name='año2_historico',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialmetrica',
            name='mes_historico',
            field=models.CharField(blank=True, choices=[('Enero', 'Enero'), ('Febrero', 'Febrero'), ('Marzo', 'Marzo'), ('Abril', 'Abril'), ('Mayo', 'Mayo'), ('Junio', 'Junio'), ('Julio', 'Julio'), ('Agosto', 'Agosto'), ('Septiembre', 'Septiembre'), ('Octubre', 'Octubre'), ('Noviembre', 'Noviembre'), ('Diciembre', 'Diciembre')], max_length=10, null=True, verbose_name='Ingrese mes:'),
        ),
        migrations.AddField(
            model_name='historialmetrica',
            name='semestre_historico',
            field=models.CharField(blank=True, choices=[('Enero-Junio', 'Enero-Junio'), ('Julio-Diciembre', 'Julio-Diciembre')], max_length=15, null=True, verbose_name='Ingrese semestre:'),
        ),
    ]