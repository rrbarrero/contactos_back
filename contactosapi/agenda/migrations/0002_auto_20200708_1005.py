# Generated by Django 3.0.6 on 2020-07-08 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correo',
            name='nota',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Nota'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='otrocontacto',
            name='nota',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Nota'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='telefono',
            name='nota',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Nota'),
            preserve_default=False,
        ),
    ]