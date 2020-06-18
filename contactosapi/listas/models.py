from django.db import models
from agenda.models import Cargo

class Lista(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre', unique=True)
    contactos = models.ManyToManyField(Cargo)
    descripcion = models.CharField(max_length=255, verbose_name='Descripción')

    class Meta:
        db_table = 'listas'
        verbose_name_plural = 'Listas'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.nombre)


