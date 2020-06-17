from agenda.serializers import CargoSerializer
from marcas.models import Marca

from rest_framework import serializers

class MarcaSerializer(serializers.HyperlinkedModelSerializer):

    # FIXME: no funciona el many 2 many
    # contactos = CargoSerializer()

    class Meta:
        model = Marca
        fields = ['id', 'nombre']
