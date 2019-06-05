# Generated by Django 2.2.1 on 2019-06-05 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HSH', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='mi_perfil',
        ),
        migrations.AddField(
            model_name='perfil',
            name='vencimiento_creditos',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='fecha_nacimiento',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='fecha_vencimiento_tarjeta',
            field=models.DateField(null=True),
        ),
    ]