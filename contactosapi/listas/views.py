from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics, serializers, status

from agenda.serializers import CargoSerializer
from contactosapi.settings.base import REST_FRAMEWORK

from .serializers import ListaSerializer
from .models import Lista
from agenda.models import Cargo
from listas.serializers import ListaSerializerOnlyRelatedIds


class ListaList(generics.ListAPIView):
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer

    def get(self, request):
        """En lugar de devolver las instancias completas de Cargo, devolvemos
        solo sus ids. En caso contrario, la consulta se eterniza y no necesitamos
        ahora esa info"""
        qs = Lista.objects.all()
        simple_related = bool(self.request.query_params.get("simple_related", None))
        serializer_class = ListaSerializer
        if simple_related:
            serializer_class = ListaSerializerOnlyRelatedIds
        serializer = serializer_class(qs, many=True)
        return Response(
            {"results": self.paginate_queryset(serializer.data), "count": len(qs)}
        )

    def post(self, request):
        lista = ListaSerializer(data=request.data, partial=True)
        if lista.is_valid():
            lista.save()
            return Response(lista.data)
        return Response(lista.errors, status=status.HTTP_400_BAD_REQUEST)


class ListaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer


class ListaCargos(generics.ListAPIView):
    serializer_class = CargoSerializer

    def get(self, request, pk):
        self.pk = pk
        qs = self.get_queryset()
        serializer = CargoSerializer(qs, many=True)
        return Response(
            {
                "results": serializer.data,
                "count": self.result_count,
            }
        )

    def put(self, request, pk, format=None):
        lista = Lista.objects.get(pk=pk)
        for _cargo in request.data["lista"]["contactos"]:
            cargo = Cargo.objects.get(pk=_cargo["id"])
            lista.contactos.add(cargo)
        return Response(ListaSerializer(lista).data)

    def post(self, request, pk, format=None):
        lista = Lista.objects.get(pk=pk)
        for _cargo in request.data["lista"]["contactos"]:
            cargo = Cargo.objects.get(pk=_cargo["id"])
            lista.contactos.remove(cargo)
        return Response(ListaSerializer(lista).data)

    def get_queryset(self):
        queryset = Lista.objects.get(pk=self.pk).contactos.all()
        self.result_count = len(queryset)
        return self.paginate_queryset(queryset)
