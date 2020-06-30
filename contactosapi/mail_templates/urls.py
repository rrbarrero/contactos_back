from django.urls import path, include
from rest_framework import routers
from mail_templates import views

urlpatterns =[
    path('plantillas/', views.PlantillaList.as_view()),
    path('plantillas/<int:pk>', views.PlantillaDetail.as_view()),
]