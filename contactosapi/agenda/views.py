from itertools import chain
import datetime

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404
from django.db.models import Q

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


class ColectivoSubcolectivo(generics.ListAPIView):

    def get(self, request, pk):
        self.pk = pk
        qs = self.get_queryset()
        serializer = SubColectivoSerializer(qs, many=True)
        return Response({
           'results': serializer.data,
            'count': self.result_count, 
        })
    
    def get_queryset(self):
        queryset = Colectivo.objects.get(pk=self.pk).subcolectivos.all()
        self.result_count = len(queryset)
        return self.paginate_queryset(queryset)
        


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
    serializer_class = PersonaSerializer

    def get(self, request):
        queryset = Persona.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        apellidos = self.request.query_params.get('apellidos', None)
        if nombre and apellidos:
            try:
                qs = Persona.objects.get(nombre=nombre, apellidos=apellidos)
            except Persona.DoesNotExist:
                qs = Persona()
            serializer = PersonaSerializer(qs)
            return Response(serializer.data)
        return queryset

    def post(self, request, format=None):
        nombre = request.data['nombre']
        apellidos = request.data['apellidos']
        tratamiento_data = TratamientoSerializer(data=request.data['tratamiento']).initial_data
        tratamiento = Tratamiento.objects.get(**tratamiento_data)
        try:
            persona = Persona.objects.get(nombre=nombre, apellidos=apellidos)
        except Persona.DoesNotExist:
            persona = Persona()
            persona.nombre = nombre
            persona.apellidos = apellidos
            persona.tratamiento = tratamiento
            persona.save()
        return Response(PersonaSerializer(persona).data)
        



class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class CargoList(generics.ListCreateAPIView):
    serializer_class = CargoSerializer

    def get_queryset(self):
        queryset = Cargo.objects.all()
        pk = self.request.query_params.get('pk', None)
        searchStr = self.request.query_params.get('searchStr', None)
        colectivos = self.request.query_params.get('colectivos', None)
        
        if pk:
            queryset = queryset.filter(id=int(pk))  
        elif searchStr is not None:
            persona_queryset = self._search_persona(searchStr)
            cargo_queryset = self._search_cargos(searchStr)
            queryset = list(chain(persona_queryset, cargo_queryset))
        elif colectivos is not None and colectivos.strip():
            queryset = queryset.filter(colectivo__in=colectivos.split(','))
        return queryset
    
    def _search_cargos(self, searchStr):
        query =Q()
        for word in searchStr.split():
            query |= Q(cargo__icontains=word)
            query |= Q(empresa__icontains=word)
        return Cargo.objects.filter(query)

    def _search_persona(self, searchStr):
        # FIXME: Con dos apellidos no funciona. Por ej. garcia ferreras
        query =Q()
        data = searchStr.split()
        if len(data) >= 2: # nombre y apellidos
            return Cargo.objects\
                .filter(persona__nombre__icontains=data[0])\
                .filter(persona__apellidos__icontains=" ".join(data[1:]))
        else:
            for word in data:
                query |= Q(persona__nombre__icontains=word)
                query |= Q(persona__apellidos__icontains=word)
        return Cargo.objects.filter(query)

    def post(self, request, format=None):
        cargo_nombre = request.data['cargo']
        ciudad = request.data['ciudad']
        cod_postal = request.data['codPostal']
        direccion = request.data['direccion']
        empresa = request.data['empresa']
        try:
            fecha_cese = datetime.datetime.strptime(request.data['fechaCese'],"%Y-%m-%dT%H:%M:%S.%fZ").date()
        except ValueError:
            fecha_cese = None
        finalizado = request.data['finalizado']
        notas = request.data['notas']
        colectivo_data = ColectivoSerializer(data=request.data['colectivo']).initial_data
        colectivo = Colectivo.objects.get(pk=colectivo_data['id'])
        pais_data = PaisSerializer(data=request.data['pais']).initial_data
        pais = Pais.objects.get(pk=pais_data['id'])
        persona_data = PersonaSerializer(data=request.data['persona']).initial_data
        persona = Persona.objects.get(pk=persona_data['id'])
        provincia_data = ProvinciaSerializer(data=request.data['provincia']).initial_data
        provincia = Provincia.objects.get(pk=provincia_data['id'])
        subcolectivo_data = SubColectivoSerializer(data=request.data['subcolectivo']).initial_data
        try:
            subcolectivo = SubColectivo.objects.get(pk=subcolectivo_data['id'])
        except TypeError:
            subcolectivo = None
        try:
            cargo = Cargo.objects.get(cargo=cargo_nombre, empresa=empresa, persona=persona)
        except Cargo.DoesNotExist:
            cargo = Cargo()
            cargo.cargo = cargo_nombre
            cargo.ciudad = ciudad
            cargo.cod_postal = cod_postal
            cargo.direccion = direccion
            cargo.empresa = empresa
            cargo.fecha_cese = fecha_cese
            cargo.finalizado = finalizado
            cargo.notas = notas
            cargo.colectivo = colectivo
            cargo.pais = pais
            cargo.persona = persona
            cargo.provincia = provincia
            cargo.subcolectivo = subcolectivo
            cargo.usuario_modificacion = request.user
            cargo.save()
        return Response(CargoSerializer(cargo).data)




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
