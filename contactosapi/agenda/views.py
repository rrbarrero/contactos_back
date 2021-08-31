from itertools import chain
import datetime

from rest_framework import status
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filters import rest_framework as filters
from agenda.filters import CargoFilter

from django.contrib.auth.models import User
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
from agenda.serializers import UserSerializer


def helper_format_angular_date(dateString: str) -> datetime.datetime:
    try:
        _date = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    except ValueError:
        return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
    return _date + datetime.timedelta(days=1)


class ColectivoList(generics.ListCreateAPIView):
    queryset = Colectivo.objects.all()
    serializer_class = ColectivoSerializer


class ColectivoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colectivo.objects.all()
    serializer_class = ColectivoSerializer


class SubColectivoList(generics.ListCreateAPIView):
    queryset = SubColectivo.objects.all()
    serializer_class = SubColectivoSerializer


class ColectivoSubcolectivo(generics.ListAPIView):
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
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CargoFilter

    def get_queryset(self):
        colectivos_filter_ids = self.request.GET.getlist("colectivos[]")
        if colectivos_filter_ids:
            return Cargo.objects.filter(colectivo__in=colectivos_filter_ids)
        return Cargo.objects.all()

    def post(self, request):
        data = request.data.copy()
        data["usuario_modifacion"] = request.user.id
        serializer = CargoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class Buscar(generics.ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def list(self, request):
        queryset = self.get_queryset()
        termino1 = self.request.query_params.get("termino1")
        termino2 = self.request.query_params.get("termino2")
        queryset = Persona.busca_persona(queryset, termino1, termino2)
        queryset = Cargo.busca_cargo(queryset, termino1, termino2)
        serializer = PersonaSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    """Lista usuarios"""

    def get(self, request, format=None):
        current_user = request.user
        serializer = UserSerializer(current_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
