# Generated by Django 2.2.2 on 2019-07-13 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HSH', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotsale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.FloatField()),
                ('esta_programado', models.BooleanField(default=True)),
                ('id_reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HSH.Reserva')),
            ],
        ),
    ]