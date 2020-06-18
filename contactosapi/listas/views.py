from django.shortcuts import render

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView


from .serializers import ListaSerializer
from .models import Lista

class ListaList(generics.ListCreateAPIView):
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer
    
class ListaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer
