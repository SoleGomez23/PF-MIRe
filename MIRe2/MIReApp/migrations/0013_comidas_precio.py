# Generated by Django 3.2.20 on 2023-09-19 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIReApp', '0012_auto_20230919_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='comidas',
            name='precio',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]
