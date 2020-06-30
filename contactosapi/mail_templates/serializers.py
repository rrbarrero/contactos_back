from rest_framework import serializers

from mail_templates.models import Plantilla

class PlantillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plantilla
        fields = ['id', 'nombre', 'asunto', 'body_content']