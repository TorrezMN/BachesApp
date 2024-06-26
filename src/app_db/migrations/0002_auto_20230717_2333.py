# Generated by Django 3.1.3 on 2023-07-17 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='is_fast_record',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registro',
            name='material_type_road',
            field=models.IntegerField(choices=[(0, 'Reg. Rapido'), (1, 'asfaltado'), (2, 'tierra'), (3, 'piedra')], default=3, help_text='Seleccione el tipo de material del camino.', null=True, verbose_name='Tipo de Material'),
        ),
        migrations.AlterField(
            model_name='registro',
            name='road_type',
            field=models.IntegerField(choices=[(0, 'Reg. Rapido'), (1, 'ruta'), (2, 'vecinal'), (3, 'nacional')], default=2, help_text='Seleccione el tipo de camino.', null=True, verbose_name='Tipo de Camino'),
        ),
        migrations.AlterField(
            model_name='registro',
            name='type_of_traffic',
            field=models.IntegerField(choices=[(0, 'Reg. Rapido'), (1, 'mucho'), (2, 'poco'), (3, 'bajo')], default=2, help_text='Seleccione el tipo de trafico.', null=True, verbose_name='Tipo de Trafico'),
        ),
    ]
