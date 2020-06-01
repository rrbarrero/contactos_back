from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Colectivo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre', unique=True)

    class Meta:
        db_table = 'colectivos'
        verbose_name_plural = 'Colectivos'

    def __str__(self):
        return "{}".format(self.nombre)

class SubColectivo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    colectivo = models.ForeignKey(Colectivo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subcolectivos'
        verbose_name_plural = 'SubColectivos'
        unique_together = ('nombre', 'colectivo')

    def __str__(self):
        return "{}".format(self.nombre)


class Pais(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre', unique=True)

    class Meta:
        db_table = 'paises'
        verbose_name_plural = 'Paises'

    def __str__(self):
        return "{}".format(self.nombre)


class Tratamiento(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre', unique=True)

    class Meta:
        db_table = 'tratamientos'
        verbose_name_plural = 'Tratamientos'

    def __str__(self):
        return "{}".format(self.nombre)


class Provincia(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre', unique=True)

    class Meta:
        db_table = 'provincias'
        verbose_name_plural = 'Provincias'

    def __str__(self):
        return "{}".format(self.nombre)


class Persona(models.Model):
    nombre = models.CharField(max_length=500, verbose_name='Nombre')
    apellidos = models.CharField(max_length=500, verbose_name='Apellidos', null=True)
    tratamiento = models.ForeignKey(Tratamiento, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'personas'
        verbose_name_plural = 'Personas'
        unique_together = ('nombre', 'apellidos')

    def __str__(self):
        return "{apellidos}, {nombre}".format(nombre=self.nombre, apellidos=self.apellidos)



class Cargo(models.Model):
    cargo = models.CharField(max_length=500, verbose_name='Cargo')
    persona = models.ForeignKey(Persona, verbose_name='Persona', on_delete=models.CASCADE)
    finalizado = models.BooleanField()
    ciudad = models.CharField(max_length=500, verbose_name='Ciudad')
    cod_postal = models.CharField(max_length=5, verbose_name='Código Postal')
    direccion = models.CharField(max_length=500, verbose_name='Dirección')
    provincia = models.ForeignKey(Provincia, verbose_name ='Provincia', on_delete=models.PROTECT)
    pais = models.ForeignKey(Pais, verbose_name="Pais", on_delete=models.PROTECT)
    empresa = models.CharField(max_length=500, verbose_name='Empresa')
    fecha_cese = models.DateField(blank=True, verbose_name='Fecha finalización del cargo', null=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    colectivo = models.ForeignKey(Colectivo, on_delete=models.PROTECT)
    subcolectivo = models.ForeignKey(SubColectivo, on_delete=models.PROTECT)
    usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    notas = models.TextField(null=True)

    class Meta:
        db_table = 'cargos'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return "{tratamiento} {apellidos}, {nombre} <{cargo} en {empresa}>".format(
            nombre=self.persona.nombre, 
            apellidos=self.persona.apellidos, 
            cargo=self.cargo,
            empresa=self.empresa,
            tratamiento=self.persona.tratamiento,
        )