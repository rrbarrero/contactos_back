from itertools import chain
import hashlib

from django.conf import settings
from django.db import models
from django.db.models import Q

# from django.db.models.signals import post_save
from django.dispatch import receiver
from iteration_utilities import unique_everseen

# from rest_framework.authtoken.models import Token


def md5Hash(keyStr):
    data = (keyStr).encode("utf8")
    return hashlib.md5(data).hexdigest()


class Colectivo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    class Meta:
        db_table = "colectivos"
        verbose_name_plural = "Colectivos"
        ordering = ["id"]

    def __str__(self):
        return "{}".format(self.nombre)


class SubColectivo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    colectivo = models.ForeignKey(
        Colectivo, on_delete=models.CASCADE, related_name="subcolectivos"
    )
    unique_key = models.CharField(
        max_length=255, verbose_name="Unique key", unique=True
    )

    class Meta:
        db_table = "subcolectivos"
        verbose_name_plural = "SubColectivos"
        # unique_together = ("nombre", "colectivo")
        ordering = ["id"]

    def __str__(self):
        return "{}".format(self.nombre)

    def save(self, *args, **kwargs):
        self.unique_key = md5Hash(self.nombre + self.colectivo.nombre)
        super(SubColectivo, self).save(*args, **kwargs)


class Pais(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    class Meta:
        db_table = "paises"
        verbose_name_plural = "Paises"
        ordering = ["nombre"]

    def __str__(self):
        return "{}".format(self.nombre)


class Tratamiento(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    class Meta:
        db_table = "tratamientos"
        verbose_name_plural = "Tratamientos"
        ordering = ["nombre"]

    def __str__(self):
        return "{}".format(self.nombre)


class Provincia(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    class Meta:
        db_table = "provincias"
        verbose_name_plural = "Provincias"
        ordering = ["nombre"]

    def __str__(self):
        return "{}".format(self.nombre)


class Persona(models.Model):
    nombre = models.CharField(max_length=500, verbose_name="Nombre")
    apellidos = models.CharField(max_length=500, verbose_name="Apellidos", null=True)
    tratamiento = models.ForeignKey(
        Tratamiento, blank=True, null=True, on_delete=models.SET_NULL
    )
    unique_key = models.CharField(
        max_length=255, verbose_name="Unique key", unique=True
    )
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "personas"
        verbose_name_plural = "Personas"
        # unique_together = ("nombre", "apellidos")
        ordering = ["-fecha_alta"]

    def __str__(self):
        return "{apellidos}, {nombre}".format(
            nombre=self.nombre, apellidos=self.apellidos
        )

    def save(self, *args, **kwargs):
        self.unique_key = md5Hash(self.nombre + self.apellidos)
        super(Persona, self).save(*args, **kwargs)

    @staticmethod
    def busca_persona(queryset, termino1, termino2):
        """Busca en nombre y apellidos por termino1 y termino2"""
        if not termino1 and not termino2:
            return queryset
        result_1 = []
        result_2 = []
        if termino1:
            result_1 = queryset.filter(
                Q(nombre__icontains=termino1) | Q(apellidos__icontains=termino1)
            )
        if termino2:
            result_2 = queryset.filter(
                Q(nombre__icontains=termino2) | Q(apellidos__icontains=termino2)
            )
        return list(unique_everseen(chain(result_1, result_2)))


class Cargo(models.Model):
    cargo = models.CharField(max_length=500, verbose_name="Cargo")
    persona = models.ForeignKey(
        Persona, verbose_name="Persona", on_delete=models.CASCADE, related_name="cargos"
    )
    finalizado = models.BooleanField()
    ciudad = models.CharField(max_length=500, verbose_name="Ciudad", blank=True)
    cod_postal = models.CharField(
        max_length=5, verbose_name="Código Postal", blank=True
    )
    direccion = models.CharField(max_length=500, verbose_name="Dirección", blank=True)
    provincia = models.ForeignKey(
        Provincia, verbose_name="Provincia", on_delete=models.PROTECT
    )
    pais = models.ForeignKey(Pais, verbose_name="Pais", on_delete=models.PROTECT)
    empresa = models.CharField(max_length=500, verbose_name="Empresa")
    fecha_cese = models.DateField(
        blank=True, verbose_name="Fecha finalización del cargo", null=True
    )
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    colectivo = models.ForeignKey(Colectivo, on_delete=models.PROTECT)
    subcolectivo = models.ForeignKey(SubColectivo, on_delete=models.PROTECT, null=True)
    usuario_modificacion = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    notas = models.TextField(blank=True)
    unique_key = models.CharField(
        max_length=255, verbose_name="Unique key", unique=True
    )

    class Meta:
        db_table = "cargos"
        verbose_name_plural = "Cargos"
        # unique_together = ("cargo", "persona", "empresa")
        ordering = ["-fecha_alta"]

    def __str__(self):
        return "{}".format(self.empresa)

    def save(self, *args, **kwargs):
        self.unique_key = md5Hash(
            self.cargo + self.persona.nombre + self.persona.apellidos + self.empresa
        )
        super(Cargo, self).save(*args, **kwargs)

    @staticmethod
    def busca_cargo(queryset, termino1, termino2):
        """Busca en cargos y devuelve Persona(s) con ese cargo"""
        if not termino1 and not termino2:
            return queryset
        cargos = Cargo.objects.all()
        result_1 = []
        result_2 = []
        if termino1:
            search_term1 = cargos.filter(
                Q(empresa__icontains=termino1) | Q(cargo__icontains=termino1)
            )
            result_1 = [cargo.persona for cargo in search_term1]
        if termino2:
            search_term2 = cargos.filter(
                Q(empresa__icontains=termino2) | Q(cargo__icontains=termino2)
            )
            result_2 = [cargo.persona for cargo in search_term2]
        return list(unique_everseen(chain(queryset, result_1, result_2)))


class Telefono(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="telefonos")
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    numero = models.CharField(max_length=255, verbose_name="Número de telf.")
    nota = models.CharField(max_length=255, verbose_name="Nota", blank=True)

    class Meta:
        db_table = "telefonos"
        verbose_name_plural = "Teléfonos"
        ordering = ["nombre"]

    def __str__(self):
        return "{telf} {contacto}, {cargo} ".format(
            contacto=self.cargo.persona.nombre + " " + self.cargo.persona.apellidos,
            cargo=self.cargo.cargo,
            telf=self.numero,
        )


class Correo(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="correos")
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    email = models.EmailField(verbose_name="E-mail")
    nota = models.CharField(max_length=255, verbose_name="Nota", blank=True)

    class Meta:
        db_table = "correos"
        verbose_name_plural = "Correos"
        ordering = ["nombre"]

    def __str__(self):
        return "{correo} <{contacto}, {cargo}> ".format(
            contacto=self.cargo.persona.nombre + " " + self.cargo.persona.apellidos,
            cargo=self.cargo.cargo,
            correo=self.email,
        )


class OtroContacto(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    dato = models.CharField(max_length=255, verbose_name="Dato de contacto")
    nota = models.CharField(max_length=255, verbose_name="Nota", blank=True)

    class Meta:
        db_table = "otros_contactos"
        verbose_name = "Otro contacto"
        verbose_name_plural = "Otros contactos"
        ordering = ["nombre"]


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
