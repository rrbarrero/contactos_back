# Generated by Django 3.2.4 on 2021-09-21 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_auto_20210920_1907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persona',
            options={'ordering': ['-fecha_alta'], 'verbose_name_plural': 'Personas'},
        ),
    ]
