import datetime
from visago.models import CustomUser as User
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
    tratamiento = serializers.PrimaryKeyRelatedField(queryset=Tratamiento.objects.all())

    class Meta:
        model = Persona
        fields = ["id", "nombre", "apellidos", "cargos", "tratamiento"]
        read_only_fields = [
            "id",
            "cargos",
        ]


class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ["id", "cargo", "nombre", "numero", "nota"]


class CorreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correo
        fields = ["id", "cargo", "nombre", "email", "nota"]


class CargoSerializerWrite(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
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
    telefonos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    correos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Cargo
        fields = "__all__"
        read_only_fields = [
            "unique_key",
        ]


class CargoSerializerRead(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    persona = PersonaSerializer(read_only=True)
    provincia = serializers.PrimaryKeyRelatedField(queryset=Provincia.objects.all())
    pais = serializers.PrimaryKeyRelatedField(queryset=Pais.objects.all())
    colectivo = serializers.PrimaryKeyRelatedField(queryset=Colectivo.objects.all())
    subcolectivo = serializers.PrimaryKeyRelatedField(
        queryset=SubColectivo.objects.all()
    )
    usuario_modificacion = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    telefonos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    correos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Cargo
        fields = "__all__"
