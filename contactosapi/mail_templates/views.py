from django.shortcuts import render
from rest_framework import generics

from mail_templates.models import Plantilla
from mail_templates.models import Campo
from mail_templates.serializers import PlantillaSerializer
from mail_templates.serializers import CampoSerializer

class PlantillaList(generics.ListCreateAPIView):
    queryset = Plantilla.objects.all()
    serializer_class = PlantillaSerializer

class PlantillaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plantilla.objects.all()
    serializer_class = PlantillaSerializer

class CampoList(generics.ListAPIView):
    queryset = Campo.objects.all()
    serializer_class = CampoSerializer
