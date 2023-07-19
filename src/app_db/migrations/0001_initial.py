# Generated by Django 3.1.3 on 2021-04-27 23:24

import app_db.models
from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', app_db.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contact_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('message_body', models.CharField(max_length=500, verbose_name='Mensaje')),
                ('contact_requests_status', models.IntegerField(blank=True, choices=[(1, 'Visto'), (2, 'Pendiente'), (3, 'Importante')], default=2)),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha del Mensaje')),
            ],
        ),
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(blank=True, max_length=50, verbose_name='Nombre')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Apellido')),
                ('education_level', models.IntegerField(choices=[(1, 'Primario'), (2, 'Secundario'), (3, 'Universitario')], default=3, verbose_name='Nivel Educativo')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Edad')),
                ('interest', models.CharField(blank=True, max_length=1500, verbose_name='Cual es su interes en el sitio?')),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pothole_diameter', models.FloatField(verbose_name='Diametro')),
                ('pothole_depth', models.FloatField(verbose_name='Profundidad')),
                ('pothole_quantity', models.IntegerField(verbose_name='Cantidad')),
                ('material_type_road', models.IntegerField(choices=[(1, 'asfaltado'), (2, 'tierra'), (3, 'piedra')], default=3, help_text='Seleccione el tipo de material del camino.', null=True, verbose_name='Tipo de Material')),
                ('road_type', models.IntegerField(choices=[(1, 'ruta'), (2, 'vecinal'), (3, 'nacional')], default=2, help_text='Seleccione el tipo de camino.', null=True, verbose_name='Tipo de Camino')),
                ('type_of_traffic', models.IntegerField(choices=[(1, 'mucho'), (2, 'poco'), (3, 'bajo')], default=2, help_text='Seleccione el tipo de trafico.', null=True, verbose_name='Tipo de Trafico')),
                ('pothole_coordinates', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0.0, 0.0), geography=True, srid=4326)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Caracteristicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caracteristica_estado', models.IntegerField(choices=[(0, 'Recibido'), (1, 'Visto'), (2, 'Confirmado'), (3, 'en desarrollo'), (4, 'en produccion'), (5, 'Rechazado')], default=0, verbose_name='Estado')),
                ('descripcion', models.CharField(max_length=500, verbose_name='Descripcion')),
                ('caracteristica_registered_date', models.DateTimeField(auto_now_add=True)),
                ('usuario_solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]