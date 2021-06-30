import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

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


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "content_type", "codename"]


class GroupSerializer(serializers.ModelSerializer):

    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]


class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True, read_only=True)
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "groups", "user_permissions"]


class ColectivoSerializer(serializers.HyperlinkedModelSerializer):

    subcolectivos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Colectivo
        fields = ["id", "nombre", "subcolectivos"]


class SubColectivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubColectivo
        fields = ["id", "nombre", "colectivo"]


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ["id", "nombre"]


class TratamientoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tratamiento
        fields = ["id", "nombre"]


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ["id", "nombre"]


class PersonaSerializer(serializers.HyperlinkedModelSerializer):

    cargos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tratamiento = TratamientoSerializer()

    class Meta:
        model = Persona
        fields = ["id", "nombre", "apellidos", "tratamiento", "cargos"]


class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ["id", "cargo", "nombre", "numero", "nota"]


class CorreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correo
        fields = ["id", "cargo", "nombre", "email", "nota"]


class CargoSerializer(serializers.HyperlinkedModelSerializer):

    persona = serializers.PrimaryKeyRelatedField(queryset=Persona.objects.all())
    provincia = serializers.PrimaryKeyRelatedField(queryset=Provincia.objects.all())
    pais = serializers.PrimaryKeyRelatedField(queryset=Pais.objects.all())
    colectivo = serializers.PrimaryKeyRelatedField(queryset=Colectivo.objects.all())
    subcolectivo = serializers.PrimaryKeyRelatedField(
        queryset=SubColectivo.objects.all()
    )
    usuario_modificacion = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    telefonos = serializers.PrimaryKeyRelatedField(
        queryset=Telefono.objects.all(), many=True
    )
    correos = serializers.PrimaryKeyRelatedField(
        queryset=Correo.objects.all(), many=True
    )

    class Meta:
        model = Cargo
        fields = [
            "id",
            "cargo",
            "persona",
            "finalizado",
            "ciudad",
            "cod_postal",
            "direccion",
            "provincia",
            "pais",
            "empresa",
            "fecha_cese",
            "fecha_alta",
            "fecha_modificacion",
            "colectivo",
            "subcolectivo",
            "usuario_modificacion",
            "notas",
            "telefonos",
            "correos",
        ]

    # def update(self, instance, validated_data):
    #     instance.cargo = validated_data.get("cargo", instance.cargo)
    #     instance.ciudad = validated_data.get("ciudad", instance.ciudad)
    #     instance.cod_postal = validated_data.get("cod_postal", instance.cod_postal)
    #     instance.direccion = validated_data.get("direccion", instance.direccion)
    #     instance.empresa = validated_data.get("empresa", instance.empresa)
    #     instance.fecha_cese = validated_data.get("fecha_cese", instance.fecha_cese)
    #     instance.fecha_modificacion = datetime.datetime.now()
    #     instance.finalizado = validated_data.get("finalizado", instance.finalizado)
    #     instance.notas = validated_data.get("notas", instance.notas)
    #     instance.save()
    #     return instance
