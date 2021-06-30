from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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

    class Meta:
        db_table = "subcolectivos"
        verbose_name_plural = "SubColectivos"
        unique_together = ("nombre", "colectivo")
        ordering = ["id"]

    def __str__(self):
        return "{}".format(self.nombre)


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

    class Meta:
        db_table = "personas"
        verbose_name_plural = "Personas"
        unique_together = ("nombre", "apellidos")
        ordering = ["apellidos", "nombre"]

    def __str__(self):
        return "{apellidos}, {nombre}".format(
            nombre=self.nombre, apellidos=self.apellidos
        )


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

    class Meta:
        db_table = "cargos"
        verbose_name_plural = "Cargos"
        unique_together = ("cargo", "persona", "empresa")
        ordering = ["-fecha_alta"]

    def __str__(self):
        return "{}".format(self.empresa)
        # return "{tratamiento} {apellidos}, {nombre} <{cargo}, {empresa}>".format(
        #     nombre=self.persona,
        #     apellidos=self.persona.apellidos,
        #     cargo=self.cargo,
        #     empresa=self.empresa,
        #     tratamiento=self.persona.tratamiento,
        # )


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
