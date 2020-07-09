from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from mail_templates.models import Plantilla
from mail_templates.serializers import PlantillaSerializer

class PlantillaList(generics.ListCreateAPIView):
    queryset = Plantilla.objects.all()
    serializer_class = PlantillaSerializer

    def post(self, request):
        request.data['body_content'] = request.data['bodyContent']
        plantilla = PlantillaSerializer(data=request.data)
        if plantilla.is_valid():
            plantilla.save()
            return Response(plantilla.data)
        return Response(plantilla.errors, status=status.HTTP_400_BAD_REQUEST)

class PlantillaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plantilla.objects.all()
    serializer_class = PlantillaSerializer
