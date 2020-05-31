# Generated by Django 3.0.6 on 2020-05-29 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='pais',
            field=models.ForeignKey(default=65, on_delete=django.db.models.deletion.PROTECT, to='agenda.Pais', verbose_name='Pais'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cargo',
            name='provincia',
            field=models.ForeignKey(default=45, on_delete=django.db.models.deletion.PROTECT, to='agenda.Provincia', verbose_name='Provincia'),
            preserve_default=False,
        ),
    ]
