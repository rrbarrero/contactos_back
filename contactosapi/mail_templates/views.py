from django.shortcuts import render
from rest_framework import generics

from mail_templates.models import Plantilla
from mail_templates.serializers import PlantillaSerializer

class PlantillaList(generics.ListCreateAPIView):
    queryset = Plantilla.objects.all()
    serializer_class = PlantillaSerializer

class PlantillaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plantilla.objects.all()
    serializer_class = PlantillaSerializer
