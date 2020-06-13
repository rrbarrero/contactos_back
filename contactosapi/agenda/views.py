from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView

from django.http import Http404

from agenda.models import Colectivo
from agenda.models import SubColectivo
from agenda.models import Pais
from agenda.models import Tratamiento
from agenda.models import Provincia
from agenda.models import Persona
from agenda.models import Cargo
from agenda.models import Telefono
from agenda.models import Correo

from agenda.serializers import ColectivoSerializer
from agenda.serializers import SubColectivoSerializer
from agenda.serializers import PaisSerializer
from agenda.serializers import TratamientoSerializer
from agenda.serializers import ProvinciaSerializer
from agenda.serializers import PersonaSerializer
from agenda.serializers import CargoSerializer
from agenda.serializers import TelefonoSerializer
from agenda.serializers import CorreoSerializer


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


class PaisList(generics.ListCreateAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class PaisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class TratamientoList(generics.ListCreateAPIView):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer


class TratamientoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer


class ProvinciaList(generics.ListCreateAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer


class ProvinciaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer


class PersonaList(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class CargoList(generics.ListCreateAPIView):
    serializer_class = CargoSerializer

    def get_queryset(self):
        queryset = Cargo.objects.all()
        colectivos = self.request.query_params.get('colectivos', None)
        if colectivos is not None and colectivos.strip():
            print(colectivos)
            queryset = queryset.filter(colectivo__in=colectivos.split(','))
        return queryset
    


class CargoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class TelefonoList(generics.ListCreateAPIView):
    queryset = Telefono.objects.all()
    serializer_class = TelefonoSerializer


class TelefonoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Telefono.objects.all()
    serializer_class = TelefonoSerializer


class CorreoList(generics.ListCreateAPIView):
    queryset = Correo.objects.all()
    serializer_class = CorreoSerializer


class CorreoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Correo.objects.all()
    serializer_class = CorreoSerializer
