import sys
import django
from original_models import Tratamiento as PwTratamiento
from original_models import Provincia as PwProvincia
from original_models import Pais as PwPais
from original_models import Persona as PwPersona
from original_models import Cargo as PwCargo
from original_models import Colectivo as PwColectivo
from original_models import Subcolectivo as PwSubColectivo
from original_models import Agenda as PwAgenda
import os
import logging
import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("peewee").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


sys.path.append("/home/roberto/devel/python/contactos_backend/contactosapi/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contactosapi.settings")
django.setup()
from django.db import connection
from agenda.models import *
from visago.models import CustomUser as User


def reset_tables():
    print("Vaciando tablas...")
    Telefono.objects.all().delete()
    Cargo.objects.all().delete()
    SubColectivo.objects.all().delete()
    Colectivo.objects.all().delete()
    Persona.objects.all().delete()
    Pais.objects.all().delete()
    Provincia.objects.all().delete()
    Tratamiento.objects.all().delete()
    Correo.objects.all().delete()


def tratamientos():
    print("Importando tratamientos...")
    for t in PwTratamiento.select():
        if t.nombre:
            if t.nombre.strip():
                tratamiento = Tratamiento()
                tratamiento.nombre = t.nombre
                tratamiento.save()
                print(tratamiento)


def provincias():
    print("Importando provincias...")
    for provincia in PwProvincia.select():
        p = Provincia()
        p.nombre = provincia.nombre
        p.save()
        print(provincia.nombre)


def paises():
    print("Importando paises...")
    for p in PwPais.select():
        pais = Pais()
        pais.nombre = p.nombre
        pais.save()
        print(p.nombre)


def personas():
    print("Importando personas...")
    personas_counter = 0
    for p in PwPersona.select():
        persona = Persona()
        try:
            persona.tratamiento = Tratamiento.objects.get(nombre=p.tratamiento.nombre)
        except AttributeError:
            persona.tratamiento = None
        except django.core.exceptions.ObjectDoesNotExist:
            logger.warning("Tratamiento no encontrado {}".format(p.tratamiento.nombre))
            persona.tratamiento = None
        if p.nombre and p.nombre.strip():
            persona.nombre = p.nombre
        else:
            logger.error("Sin nombre {}".format(p.id))
            continue
        if p.apellidos and p.apellidos.strip():
            persona.apellidos = p.apellidos
        else:
            logger.warning("Persona sin apellidos. Nombre {}".format(persona.nombre))
            persona.apellidos = None
        try:
            persona.save()
            personas_counter += 1
        except django.db.utils.IntegrityError:
            ## logger.warning("Duplicada. Persona: <id: {} Nombre: {} Apellidos: {}".format(p.id, p.nombre, p.apellidos))
            continue
        except TypeError:
            logger.warning(f"Sin nombre y apellidos {p.id}")
            continue
    logger.info("PERSONAS IMPORTADAS {}.".format(personas_counter))


def colectivos():
    print("Importando colectivos...")
    for c in PwColectivo.select():
        if c.nombre and c.nombre.strip():
            colectivo = Colectivo()
            colectivo.nombre = c.nombre
            colectivo.save()
            print(colectivo)


def subcolectivos():
    print("Importando subtratamientos...")
    for c in PwSubColectivo.select():
        if c.nombre and c.nombre.strip() and c.nombre != "Sin subcolectivo":
            subcolectivo = SubColectivo()
            subcolectivo.nombre = c.nombre
            subcolectivo.colectivo = Colectivo.objects.get(
                nombre=PwColectivo.get(PwColectivo.id == c.id_colectivo).nombre
            )
            subcolectivo.save()
            print(subcolectivo)


def cargos():
    print("Importando cargos...")
    cargos_counter = 0
    for c in PwCargo.select():
        try:
            personas = Persona.objects.filter(
                nombre=c.id_persona.nombre, apellidos=c.id_persona.apellidos
            ).all()
        except django.core.exceptions.ObjectDoesNotExist:
            logger.error(
                "Persona no encontrada {} {}. Cargo {}.!!".format(
                    c.id_persona.nombre, c.id_persona.apellidos, c.cargo
                )
            )
            continue
        if len(personas) > 1:
            logger.warning(
                "Ambigüedad detectada {} {}. Cargo {}.!!".format(
                    c.id_persona.nombre, c.id_persona.apellidos, c.cargo
                )
            )
        elif len(personas) == 0:
            logger.error(
                "Persona no encontrada {} {}. Cargo {}.!!".format(
                    c.id_persona.nombre, c.id_persona.apellidos, c.cargo
                )
            )
            continue
        persona = personas[0]
        cargos = Cargo.objects.filter(
            cargo=c.cargo, empresa=c.empresa, persona=persona
        ).all()
        if len(cargos) > 0:
            continue
        cargo = Cargo()
        try:
            if cargo.id_provincia.nombre.strip():
                cargo.provincia = c.id_provincia.nombre
            else:
                cargo.provincia = Provincia.objects.get(nombre="Sin especificar")
        except:
            cargo.provincia = Provincia.objects.get(nombre="Sin especificar")
        cargo.persona = persona
        cargo.cargo = c.cargo
        cargo.finalizado = c.cargo_finalizado
        cargo.ciudad = c.ciudad
        cargo.cod_postal = c.cod_postal
        if len(c.cod_postal) > 5:
            logger.warning("Mal código postal. Cargo id viejo {}".format(c.id))
            cargo.cod_postal = "00000"
        cargo.direccion = c.direccion
        cargo.pais = Pais.objects.get(nombre=c.id_pais.nombre)
        cargo.empresa = c.empresa
        cargo.fecha_cese = c.fecha_cese
        cargo.fecha_alta = c.fecha_creacion
        cargo.fecha_modificacion = c.fecha_modificacion
        try:
            cargo.colectivo = Colectivo.objects.get(nombre=c.id_colectivo.nombre)
        except:
            logger.error("Colectivo no encontrado: {}".format(c.id_colectivo.nombre))
            continue
        try:
            cargo.subcolectivo = SubColectivo.objects.get(
                nombre=c.id_subcolectivo.nombre, colectivo=cargo.colectivo
            )
        except django.core.exceptions.ObjectDoesNotExist:
            logger.error(
                "Subcolectivo NO ENCONTRADO: nombre: {} colectivo {}".format(
                    c.id_subcolectivo.nombre, cargo.colectivo
                )
            )
            continue
        cargo.usuario_modificacion = User.objects.first()
        cargo.notas = c.notas
        cargo.save()
        cargos_counter += 1
    logger.info("CARGOS IMPORTADOS {}.".format(cargos_counter))


def telefonos():
    print("Importando teléfonos...")
    telefonos_counter = 0
    for t in PwAgenda.select().where(PwAgenda.tipo.in_([1, 2, 6])):
        nombre = t.id_cargo.id_persona.nombre
        apellidos = t.id_cargo.id_persona.apellidos
        if nombre:
            nombre = nombre.strip()
        if apellidos:
            apellidos = apellidos.strip()
        try:
            persona = Persona.objects.get(
                nombre=nombre,
                apellidos=apellidos,
            )
        except django.core.exceptions.ObjectDoesNotExist:
            logger.error(
                "Cargo cuya persona no encontrada: nombre<{}> apellidos<{}>".format(
                    nombre, apellidos
                )
            )
            continue
        cargos = Cargo.objects.filter(
            cargo=t.id_cargo.cargo.strip(),
            empresa=t.id_cargo.empresa.strip(),
            persona=persona,
        )
        if len(cargos) == 0:
            logger.error(
                "Cargo no encontrado. cargo: <{}> empresa: <{}> nombre: <{}>".format(
                    t.id_cargo.cargo.strip(),
                    t.id_cargo.empresa.strip(),
                    persona,
                )
            )
            continue
        else:
            for cargo in cargos:
                telf = Telefono()
                telf.cargo = cargo
                telf.nombre = t.nombre if t.nombre else "Sin especificar"
                telf.numero = t.dato
                telf.nota = t.info if t.info else ""
                telf.save()
                telefonos_counter += 1
    print(telefonos_counter)


def correos():
    print("Importando correos...")
    correos_counter = 0
    for t in PwAgenda.select().where(
        PwAgenda.tipo.in_(
            [
                3,
            ]
        )
    ):
        nombre = t.id_cargo.id_persona.nombre
        apellidos = t.id_cargo.id_persona.apellidos
        if nombre:
            nombre = nombre.strip()
        if apellidos:
            apellidos = apellidos.strip()
        try:
            persona = Persona.objects.get(
                nombre=nombre,
                apellidos=apellidos,
            )
        except django.core.exceptions.ObjectDoesNotExist:
            logger.error(
                "Cargo cuya persona no encontrada: nombre<{}> apellidos<{}>".format(
                    nombre, apellidos
                )
            )
            continue
        cargos = Cargo.objects.filter(
            cargo=t.id_cargo.cargo.strip(),
            empresa=t.id_cargo.empresa.strip(),
            persona=persona,
        )
        if len(cargos) == 0:
            logger.error(
                "Cargo no encontrado. cargo: <{}> empresa: <{}> nombre: <{}>".format(
                    t.id_cargo.cargo.strip(),
                    t.id_cargo.empresa.strip(),
                    persona,
                )
            )
            continue
        else:
            for cargo in cargos:
                email = Correo()
                email.cargo = cargo
                email.nombre = t.nombre if t.nombre else "Sin especificar"
                email.email = t.dato
                email.nota = t.info if t.info else ""
                email.save()
                correos_counter += 1
    print(correos_counter)


if __name__ == "__main__":
    # reset_tables()
    tratamientos()
    provincias()
    paises()
    personas()
    colectivos()
    subcolectivos()
    cargos()
    telefonos()
    correos()
