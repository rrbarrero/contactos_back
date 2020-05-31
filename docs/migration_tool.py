import sys
import django
from original_models import Provincia as PwProvincia
from original_models import Pais as PwPais
from original_models import Persona as PwPersona
from original_models import Cargo as PwCargo
import os
import logging
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logging.getLogger('peewee').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


sys.path.append('/home/roberto/devel/python/contactos_backend/contactosapi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contactosapi.settings.devel")
django.setup()

from agenda.models import *

# your imports, e.g. Django models

def provincias():
    for provincia in PwProvincia.select():
        p = Provincia()
        p.nombre = provincia.nombre
        p.save()
        print(provincia.nombre)


def paises():
    for p in PwPais.select():
        pais = Pais()
        pais.nombre = p.nombre
        pais.save()
        print(p.nombre)        

def personas():
    for p in PwPersona.select():
        persona = Persona()
        print(p.nombre, "  -  ", p.apellidos)
        try:
            persona.tratamiento = Tratamiento.objects.filter(nombre=p.tratamiento.nombre).one()
        except AttributeError:
            persona.tratamiento = None
        persona.nombre = p.nombre
        if not p.apellidos:
            persona.apellidos = "Sin especificar"
        else:
            persona.apellidos = p.apellidos
        try:
            persona.save()
        except django.db.utils.IntegrityError:
            logger.error("Persona: <id: {} Nombre: {} Apellidos: {}".format(p.id, p.nombre, p.apellidos))


def cargos():
    counter=1
    for c in PwCargo.select():
        try:
            provincia = c.id_provincia.nombre
            print(provincia)
        except PwProvincia.DoesNotExist:
            #print(counter)
            counter += 1
        # cargo = Cargo()
        # cargo.persona = Persona.objects.filter(
        #      nombre=c.id_persona.nombre,
        #      apellidos=c.id_persona.apellidos,
        # ).get()
        # cargo.cargo = c.cargo
        # cargo.finalizado = c.cargo_finalizado
        # cargo.ciudad = c.ciudad
        # cargo.cod_postal = c.cod_postal
        # cargo.direccion = c.direccion
        # cargo.provincia = Provincia.objects.filter(nombre=c.id_provincia.nombre).one()
        # cargo.pais = Pais.objects.filter(nombre=c.id_pais.nombre).one()
        # cargo.empresa = c.empresa
        # cargo.fecha_cese = c.fecha_cese
        # cargo.fecha_alta = c.fecha_creacion
        # cargo.fecha_modificacion = c.fecha_modificacion
        # cargo.colectivo = Colectivo.objects.filter(nombre=c.id_colectivo.nombre)
        # cargo.subcolectivo = SubColectivo.objects.filter(nombre=c.id_subcolectivo.nombre)
        # cargo.usuario_modificacion = 1
        # cargo.notas = c.notas 


if __name__ == '__main__':
    # provincias()
    # paises()
    # personas()
    cargos()
