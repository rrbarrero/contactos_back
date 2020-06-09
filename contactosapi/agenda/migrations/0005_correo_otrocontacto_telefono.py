# Generated by Django 3.0.6 on 2020-06-02 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0004_auto_20200601_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Telefono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
                ('numero', models.CharField(max_length=255, verbose_name='Número de telf.')),
                ('nota', models.CharField(max_length=255, verbose_name='Nota')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.Cargo')),
            ],
            options={
                'verbose_name_plural': 'Telefonos',
                'db_table': 'telefonos',
            },
        ),
        migrations.CreateModel(
            name='OtroContacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
                ('dato', models.CharField(max_length=255, verbose_name='Dato de contacto')),
                ('nota', models.CharField(max_length=255, verbose_name='Nota')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.Cargo')),
            ],
            options={
                'verbose_name': 'Otro contacto',
                'verbose_name_plural': 'Otros contactos',
                'db_table': 'otros_contactos',
            },
        ),
        migrations.CreateModel(
            name='Correo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('nota', models.CharField(max_length=255, verbose_name='Nota')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.Cargo')),
            ],
            options={
                'verbose_name_plural': 'Correos',
                'db_table': 'correos',
            },
        ),
    ]