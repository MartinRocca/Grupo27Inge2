# Generated by Django 2.2.1 on 2019-06-04 16:57

import HSH.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField()),
                ('nro_tarjeta_credito', models.IntegerField(null=True)),
                ('marca_tarjeta_credito', models.CharField(max_length=30)),
                ('nombre_titular_tarjeta', models.CharField(max_length=120)),
                ('fecha_vencimiento_tarjeta', models.DateField()),
                ('codigo_seguridad_tarjeta', models.IntegerField(null=True)),
                ('creditos', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Residencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localidad', models.CharField(max_length=150)),
                ('nombre', models.CharField(max_length=70)),
                ('descripcion', models.TextField()),
                ('precio_base', models.FloatField()),
                ('limite_personas', models.PositiveSmallIntegerField()),
                ('nro_direccion', models.PositiveIntegerField()),
                ('calle', models.CharField(max_length=100)),
                ('cant_habitaciones', models.PositiveSmallIntegerField()),
                ('imagen_URL', models.URLField()),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('is_premium', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('mi_perfil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HSH.Perfil')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', HSH.models.UsuarioManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subasta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('esta_programada', models.BooleanField(default=True)),
                ('id_reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HSH.Reserva')),
            ],
        ),
        migrations.AddField(
            model_name='reserva',
            name='id_residencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HSH.Residencia'),
        ),
        migrations.CreateModel(
            name='Puja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_usuario', models.EmailField(max_length=254)),
                ('monto', models.FloatField()),
                ('id_subasta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HSH.Subasta')),
            ],
        ),
        migrations.AddField(
            model_name='perfil',
            name='mi_usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='reserva',
            unique_together={('id_residencia', 'fecha')},
        ),
    ]
