from django.urls import path, include
from rest_framework import routers
from marcas import views


urlpatterns = [
    path('marcas/', views.MarcaList.as_view()),
]
