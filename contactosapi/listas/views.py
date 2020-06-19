from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics, status

from agenda.serializers import CargoSerializer
from contactosapi.settings.base import REST_FRAMEWORK

from .serializers import ListaSerializer
from .models import Lista
from agenda.models import Cargo

class ListaList(generics.ListCreateAPIView):
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer

    
class ListaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer


class ListaCargos(generics.ListAPIView):

    def get(self, request, pk):
        self.pk = pk
        qs = self.get_queryset()
        serializer = CargoSerializer(qs, many=True)
        return Response({
            'results': serializer.data,
            'count': self.result_count,
        })

    def put(self, request, pk, format=None):
        lista = Lista.objects.get(pk=pk)
        for _cargo in request.data['lista']['contactos']:
            cargo = Cargo.objects.get(pk=_cargo['id'])
            lista.contactos.add(cargo)
        return Response(ListaSerializer(lista).data)

    def get_queryset(self):
        queryset = Lista.objects.get(pk=self.pk).contactos.all()
        self.result_count = len(queryset)
        return self.paginate_queryset(queryset)