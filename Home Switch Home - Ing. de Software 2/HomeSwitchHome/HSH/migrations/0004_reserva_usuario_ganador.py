# Generated by Django 2.2.1 on 2019-06-18 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HSH', '0003_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='usuario_ganador',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
