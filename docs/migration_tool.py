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

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logging.getLogger('peewee').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


sys.path.append('/home/roberto/devel/python/contactos_backend/contactosapi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contactosapi.settings.devel")
django.setup()
from django.db import connection
from agenda.models import *



def tratamientos():
    Tratamiento.objects.all().delete()
    for t in PwTratamiento.select():
        if t.nombre:
            if t.nombre.strip():
                tratamiento = Tratamiento()
                tratamiento.nombre = t.nombre
                tratamiento.save()
                print(tratamiento)


def provincias():
    Provincia.objects.all().delete()
    for provincia in PwProvincia.select():
        p = Provincia()
        p.nombre = provincia.nombre
        p.save()
        print(provincia.nombre)


def paises():
    Pais.objects.all().delete()
    for p in PwPais.select():
        pais = Pais()
        pais.nombre = p.nombre
        pais.save()
        print(p.nombre)        

def personas():
    Persona.objects.all().delete()
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
            logger.warning('Persona sin apellidos. Nombre {}'.format(persona.nombre))
            persona.apellidos = None
        try:
            persona.save()
        except django.db.utils.IntegrityError:
            logger.warning("Duplicada. Persona: <id: {} Nombre: {} Apellidos: {}".format(p.id, p.nombre, p.apellidos))


def colectivos():
    Colectivo.objects.all().delete()
    for c in PwColectivo.select():
        if c.nombre and c.nombre.strip():
            colectivo = Colectivo()
            colectivo.nombre = c.nombre
            colectivo.save()
            print(colectivo)


def subcolectivos():
    SubColectivo.objects.all().delete()
    for c in PwSubColectivo.select():
        if c.nombre and c.nombre.strip() and c.nombre!='Sin subcolectivo':
            subcolectivo = SubColectivo()
            subcolectivo.nombre = c.nombre
            subcolectivo.colectivo = Colectivo.objects.get(nombre=PwColectivo.get(PwColectivo.id==c.id_colectivo).nombre)
            subcolectivo.save()
            print(subcolectivo)

def cargos():
    Cargo.objects.all().delete()
    for c in PwCargo.select():
        cargo = Cargo()
        try:
            if cargo.id_provincia.nombre.strip():
                cargo.provincia = c.id_provincia.nombre
            else:
                cargo.provincia = Provincia.objects.get(nombre="Sin especificar")
        except:
            cargo.provincia = Provincia.objects.get(nombre="Sin especificar")
        try:
            cargo.persona = Persona.objects.get(
                nombre=c.id_persona.nombre,
                apellidos=c.id_persona.apellidos,
            )
        except django.core.exceptions.MultipleObjectsReturned:
            for persona in Persona.objects.filter(nombre=c.id_persona.nombre, apellidos=c.id_persona.apellidos):
                logger.error("Ambigüedad detectada {} {}. Cargo {}.!!".format(persona.nombre, persona.apellidos, c.cargo))
            continue
        except django.core.exceptions.ObjectDoesNotExist:
            logger.error("Persona no encontrada {} {}. Cargo {}.!!".format(c.id_persona.nombre, c.id_persona.apellidos, c.cargo))
            continue
        cargo.cargo = c.cargo
        cargo.finalizado = c.cargo_finalizado
        cargo.ciudad = c.ciudad
        cargo.cod_postal = c.cod_postal
        if len(c.cod_postal)>5:
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
            print(c.id_colectivo.nombre)
            sys.exit()
        try:
            cargo.subcolectivo = SubColectivo.objects.get(nombre=c.id_subcolectivo.nombre, colectivo=cargo.colectivo)
        except django.core.exceptions.ObjectDoesNotExist:
            logger.error("Subcolectivo NO ENCONTRADO: nombre: {} colectivo {}".format(c.id_subcolectivo.nombre, cargo.colectivo))
            print("Subcolectivo NO ENCONTRADO: nombre: {} colectivo {}".format(c.id_subcolectivo.nombre, cargo.colectivo))
            sys.exit()
        cargo.usuario_modificacion = User.objects.first()
        cargo.notas = c.notas 
        cargo.save()


def telefonos():
    Telefono.objects.all().delete()
    for t in PwAgenda.select().where(PwAgenda.tipo.in_([1,2,6])):
        nombre = t.id_cargo.id_persona.nombre.strip()
        apellidos = t.id_cargo.id_persona.apellidos.strip()
        if nombre and apellidos:
            try:
                persona = Persona.objects.get(
                    nombre=nombre,
                    apellidos=apellidos,
                )
            except django.core.exceptions.ObjectDoesNotExist:
                print(persona, apellidos)
                sys.exit()
            try:
                cargo = Cargo.objects.get(
                    cargo=t.id_cargo.cargo,
                    persona=persona,
                )
            except django.core.exceptions.ObjectDoesNotExist:
                logger.error("Cargo no encontrado. <cargo: {} persona: {}>".format(
                    t.id_cargo.cargo,
                    persona
                ))
                continue
            telf = Telefono()
            telf.cargo = cargo
            telf.nombre = t.nombre
            telf.numero = t.dato
            telf.nota = t.info
            telf.save()

    

if __name__ == '__main__':
    # tratamientos()
    # provincias()
    # paises()
    # personas()
    # colectivos()
    # subcolectivos()
    # cargos()
    telefonos()
