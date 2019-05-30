# Generated by Django 2.2.1 on 2019-05-30 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HSH', '0006_auto_20190529_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('contraseña', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=30)),
                ('fecha_nacimiento', models.DateField()),
                ('nro_tarjeta_credito', models.PositiveIntegerField()),
                ('marca_tarjeta_credito', models.CharField(max_length=20)),
                ('nombre_titular_tarjeta', models.CharField(max_length=30)),
                ('fecha_vencimiento_tarjeta', models.DateField()),
                ('codigo_seguridad_tarjeta', models.PositiveIntegerField()),
                ('creditos', models.IntegerField(default=2)),
                ('es_premium', models.BooleanField(default=False)),
            ],
        ),
    ]
