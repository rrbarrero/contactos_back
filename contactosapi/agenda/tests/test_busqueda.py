import json

from visago.models import CustomUser as User
from agenda.models import Persona, Tratamiento
from django.conf import settings
from django.db.utils import IntegrityError
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
        url = reverse("auth-login")
        response = self.client.post(
            url,
            {
                "username": settings.TESTING_VALID_AD_USERNAME,
                "password": settings.TESTING_VALID_AD_PASSWORD,
            },
            format="json",
        )
        data = json.loads(response.content)
        self.token = data["token"]

    def test_busca_por_nombre_y_primer_apellido(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("busca-contacto")
        response = self.client.get(
            url,
            {"termino1": "nombre_test_3", "termino2": "apellidos_test_3"},
            format="json",
        )
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)

    def test_busca_por_cargo_y_empresa(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("busca-contacto")
        response = self.client.get(
            url,
            {"termino1": "cargo_test_2", "termino2": "empresa_test_2"},
            format="json",
        )
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)

    def test_busca_por_cargo_y_apellidos(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("busca-contacto")
        response = self.client.get(
            url,
            {"termino1": "cargo_test_1", "termino2": "apellidos_test_1"},
            format="json",
        )
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)

    def test_busca_por_nombre_y_apellidos_diferente_persona(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("busca-contacto")
        response = self.client.get(
            url,
            {"termino1": "nombre_test_3", "termino2": "apellidos_test_2"},
            format="json",
        )
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)
