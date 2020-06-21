from django.urls import path, include
from rest_framework import routers
from agenda import views


urlpatterns = [
    path('colectivos/', views.ColectivoList.as_view()),
    path('colectivos/<int:pk>', views.ColectivoDetail.as_view()),
    path('colectivos/<int:pk>/subcolectivos', views.ColectivoSubcolectivo.as_view()),
    path('subcolectivos/', views.SubColectivoList.as_view()),
    path('subcolectivos/<int:pk>', views.SubColectivoDetail.as_view()),
    path('paises/', views.PaisList.as_view()),
    path('tratamientos/', views.TratamientoList.as_view()),
    path('provincias/', views.ProvinciaList.as_view()),
    path('personas/', views.PersonaList.as_view()),
    path('personas/<int:pk>', views.PersonaDetail.as_view()),
    path('cargos/', views.CargoList.as_view()),
    path('cargos/<int:pk>', views.CargoDetail.as_view()),
    path('telefonos/', views.TelefonoList.as_view()),
    path('correos/', views.CorreoList.as_view()),
]
