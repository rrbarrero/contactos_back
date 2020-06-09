from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView

from django.http import Http404

from agenda.models import Colectivo
from agenda.models import SubColectivo
from agenda.serializers import ColectivoSerializer
from agenda.serializers import SubColectivoSerializer


class ColectivoList(generics.ListCreateAPIView):
    queryset = Colectivo.objects.all()
    serializer_class = ColectivoSerializer
    
class ColectivoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colectivo.objects.all()
    serializer_class = ColectivoSerializer


class SubColectivoList(generics.ListCreateAPIView):
    queryset = SubColectivo.objects.all()
    serializer_class = SubColectivoSerializer


class SubColectivoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubColectivo.objects.all()
    serializer_class = SubColectivoSerializer

