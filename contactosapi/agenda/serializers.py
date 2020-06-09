from agenda.models import Colectivo
from agenda.models import SubColectivo
from rest_framework import serializers


class ColectivoSerializer(serializers.HyperlinkedModelSerializer):

    subcolectivos = serializers.StringRelatedField(many=True)

    class Meta:
        model = Colectivo
        fields = ['nombre', 'subcolectivos']

    

class SubColectivoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubColectivo
        fields = ['nombre', 'colectivo']
