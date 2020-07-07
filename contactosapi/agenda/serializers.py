import datetime
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
        fields = ['id', 'nombre', 'colectivo']


class PaisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pais
        fields = ['id', 'nombre']


class TratamientoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tratamiento
        fields = ['id', 'nombre']


class ProvinciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provincia
        fields = ['id', 'nombre']


class PersonaSerializer(serializers.HyperlinkedModelSerializer):

    cargos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tratamiento = TratamientoSerializer()

    class Meta:
        model = Persona
        fields = ['id', 'nombre', 'apellidos', 'tratamiento', 'cargos']

class TelefonoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Telefono
        fields = ['id', 'cargo', 'nombre', 'numero', 'nota']


class CorreoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Correo
        fields = ['id', 'cargo', 'nombre', 'email', 'nota']

class CargoSerializer(serializers.HyperlinkedModelSerializer):

    persona = PersonaSerializer()
    provincia = serializers.StringRelatedField()
    pais = serializers.StringRelatedField()
    colectivo = serializers.StringRelatedField()
    subcolectivo = serializers.StringRelatedField()
    usuario_modificacion = serializers.StringRelatedField()
    telefonos = TelefonoSerializer(many=True)
    correos = CorreoSerializer(many=True)

    class Meta:
        model = Cargo
        fields = ['id', 'cargo', 'persona', 'finalizado', 'ciudad', 'cod_postal', 'direccion',
             'provincia', 'pais', 'empresa', 'fecha_cese', 'fecha_alta', 'fecha_modificacion',
             'colectivo', 'subcolectivo', 'usuario_modificacion', 'notas', 'telefonos',
             'correos']

    def update(self, instance, validated_data):
        instance.cargo = validated_data.get('cargo', instance.cargo)
        instance.ciudad = validated_data.get('ciudad', instance.ciudad)
        instance.cod_postal = validated_data.get('cod_postal', instance.cod_postal)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.empresa = validated_data.get('empresa', instance.empresa)
        instance.fecha_cese = validated_data.get('fecha_cese', instance.fecha_cese)
        instance.fecha_modificacion = datetime.datetime.now()
        instance.finalizado = validated_data.get('finalizado', instance.finalizado)
        instance.notas = validated_data.get('notas', instance.notas)
        instance.save()
        return instance