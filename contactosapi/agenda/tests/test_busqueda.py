import json

from agenda.models import Persona, Tratamiento
from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase


class BusquedaTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = [
        "users.yaml",
        "tratamiento.yaml",
        "provincia.yaml",
        "persona.yaml",
        "pais.yaml",
        "colectivo.yaml",
        "subcolectivo.yaml",
        "cargo.yaml",
    ]

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_busca_por_nombre_y_primer_apellido(self):
        url = reverse("busca-contacto")
        response = self.client.get(
            url,
            {"termino1": "nombre_test_3", "termino2": "apellidos_test_3"},
            format="json",
        )
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
