# Generated by Django 2.2.1 on 2019-06-19 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HSH', '0005_usuario_fecha_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='usuario_ganador',
            field=models.EmailField(default='-', max_length=254),
        ),
    ]
