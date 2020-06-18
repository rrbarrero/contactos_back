# Generated by Django 3.0.6 on 2020-06-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agenda', '0007_auto_20200617_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Nombre')),
                ('contactos', models.ManyToManyField(to='agenda.Cargo')),
            ],
            options={
                'verbose_name_plural': 'Listas',
                'db_table': 'listas',
                'ordering': ['id'],
            },
        ),
    ]