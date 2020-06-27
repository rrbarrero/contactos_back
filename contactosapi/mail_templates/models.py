from django.db import models


class Plantilla(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre', unique=True)
    asunto = models.CharField(max_length=255, verbose_name='Asunto')
    body_content = models.TextField(verbose_name='Contenido')

    def __str__(self):
        return self.nombre


class Campo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    template_content = models.CharField(max_length=255, verbose_name='Contenido')

    def __str__(self):
        return "{}".format(self.nombre)

