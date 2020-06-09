from django.urls import path, include
from rest_framework import routers
from agenda import views


urlpatterns = [
    path('colectivos/', views.ColectivoList.as_view()),
    path('colectivos/<int:pk>', views.ColectivoDetail.as_view()),
    path('subcolectivos/', views.SubColectivoList.as_view()),
    path('subcolectivos/<int:pk>', views.SubColectivoDetail.as_view()),
#    path('colectivos/<int:pk>/subcolectivos', views.ColectivosSubColectivos.as_view()),
]
