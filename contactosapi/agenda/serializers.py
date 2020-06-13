from django.contrib.auth.models import User

from agenda.models import Colectivo
from agenda.models import SubColectivo
from agenda.models import Pais
from agenda.models import Tratamiento
from agenda.models import Provincia
from agenda.models import Persona
from agenda.models import Cargo
from agenda.models import Telefono
from agenda.models import Correo

from rest_framework import serializers


class ColectivoSerializer(serializers.HyperlinkedModelSerializer):

    subcolectivos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Colectivo
        fields = ['id', 'nombre', 'subcolectivos']

    
class SubColectivoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubColectivo
        fields = ['nombre', 'colectivo']


class PaisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pais
        fields = ['nombre']


class TratamientoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tratamiento
        fields = ['nombre']


class ProvinciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provincia
        fields = ['nombre']


class PersonaSerializer(serializers.HyperlinkedModelSerializer):

    cargos = serializers.StringRelatedField(many=True)
    tratamiento = serializers.StringRelatedField()

    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'tratamiento', 'cargos']


class CargoSerializer(serializers.HyperlinkedModelSerializer):

    persona = serializers.StringRelatedField()
    provincia = serializers.StringRelatedField()
    pais = serializers.StringRelatedField()
    colectivo = serializers.StringRelatedField()
    subcolectivo = serializers.StringRelatedField()
    usuario_modificacion = serializers.StringRelatedField()
    telefonos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    correos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Cargo
        fields = ['id', 'cargo', 'persona', 'finalizado', 'ciudad', 'cod_postal', 'direccion',
             'provincia', 'pais', 'empresa', 'fecha_cese', 'fecha_alta', 'fecha_modificacion',
             'colectivo', 'subcolectivo', 'usuario_modificacion', 'notas', 'telefonos',
             'correos']


class TelefonoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Telefono
        fields = ['cargo', 'nombre', 'numero', 'nota']


class CorreoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Correo
        fields = ['cargo', 'nombre', 'email', 'nota']
