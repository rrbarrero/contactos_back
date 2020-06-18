from django.urls import path, include
from rest_framework import routers
from listas import views


urlpatterns = [
    path('listas/', views.ListaList.as_view()),
    path('listas/<int:pk>/', views.ListaDetail.as_view()),
    path('listas/<int:pk>/cargos/', views.ListaCargos.as_view()),
]
