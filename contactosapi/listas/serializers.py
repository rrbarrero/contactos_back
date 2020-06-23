from agenda.serializers import CargoSerializer
from listas.models import Lista

from rest_framework import serializers

class ListaSerializer(serializers.HyperlinkedModelSerializer):

    contactos = CargoSerializer(many=True)

    class Meta:
        model = Lista
        fields = ['id', 'nombre', 'contactos', 'descripcion']


class ListaSerializerOnlyRelatedIds(serializers.HyperlinkedModelSerializer):
    
    contactos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Lista
        fields = ['id', 'nombre', 'contactos', 'descripcion']