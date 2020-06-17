from django.db import models
from agenda.models import Cargo

class Marca(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre', unique=True)
    contactos = models.ManyToManyField(Cargo)

    class Meta:
        db_table = 'marcas'
        verbose_name_plural = 'Marcas'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.nombre)


