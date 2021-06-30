from django.urls import path, include
from rest_framework import routers
from agenda import views


urlpatterns = [
    path("usuarios/", views.UserDetail.as_view()),
    path("colectivos/", views.ColectivoList.as_view(), name="colectivo-list"),
    path(
        "colectivos/<int:pk>", views.ColectivoDetail.as_view(), name="colectivo-detail"
    ),
    path("colectivos/<int:pk>/subcolectivos", views.ColectivoSubcolectivo.as_view()),
    path("subcolectivos/", views.SubColectivoList.as_view(), name="subcolectivo-list"),
    path(
        "subcolectivos/<int:pk>",
        views.SubColectivoDetail.as_view(),
        name="subcolectivo-detail",
    ),
    path("paises/", views.PaisList.as_view(), name="pais-list"),
    path("paises/<int:pk>", views.PaisDetail.as_view(), name="pais-detail"),
    path("tratamientos/", views.TratamientoList.as_view(), name="tratamiento-list"),
    path(
        "tratamientos/<int:pk>",
        views.TratamientoDetail.as_view(),
        name="tratamiento-detail",
    ),
    path("provincias/", views.ProvinciaList.as_view(), name="provincia-list"),
    path(
        "provincias/<int:pk>", views.ProvinciaDetail.as_view(), name="provincia-detail"
    ),
    path("personas/", views.PersonaList.as_view(), name="persona-list"),
    path("personas/<int:pk>", views.PersonaDetail.as_view(), name="persona-detail"),
    path("cargos/", views.CargoList.as_view(), name="cargo-list"),
    path("cargos/<int:pk>", views.CargoDetail.as_view(), name="cargo-detail"),
    path("telefonos/", views.TelefonoList.as_view()),
    path("correos/", views.CorreoList.as_view()),
]
