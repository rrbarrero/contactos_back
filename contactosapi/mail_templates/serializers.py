from rest_framework import serializers

from mail_templates.models import Plantilla
from mail_templates.models import Campo

class PlantillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plantilla
        fields = ['id', 'nombre', 'asunto', 'body_content']


class CampoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campo
        fields = ['id', 'nombre', 'template_content']