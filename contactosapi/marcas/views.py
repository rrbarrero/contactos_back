from django.shortcuts import render

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView


from .serializers import MarcaSerializer
from .models import Marca

class MarcaList(generics.ListCreateAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    
class MarcaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
