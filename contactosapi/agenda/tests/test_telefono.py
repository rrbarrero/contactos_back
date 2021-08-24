import json
from django.conf import settings
from django.db.utils import IntegrityError
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase
from agenda.models import Telefono


class TelefonoTestCase(APITestCase, URLPatternsTestCase):
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
        "telefono.yaml",
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

    def test_lista_telefonos_return_http_ok(self):
        """Listar telefonos devuelve http 200"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("telefono-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_telefono_return_len_ok(self):
        """Crear telefono"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("telefono-list")
        self.client.post(
            url,
            {
                "cargo": 1,
                "nombre": "telefono_test_7",
                "numero": "987654327",
                "nota": "nota_test_7",
            },
            format="json",
        )
        self.client.post(
            url,
            {
                "cargo": 1,
                "nombre": "telefono_test_8",
                "numero": "987654328",
                "nota": "nota_test_8",
            },
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 8)

    def test_elimina_telefono_return_len_ok(self):
        """Elimina telefono"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        list_url = reverse("telefono-list")
        telefono = Telefono.objects.first()
        url = reverse("telefono-detail", args=(telefono.id,))
        self.client.delete(url)
        response = self.client.get(list_url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 5)

    def test_actualiza_un_telefono_return_details_ok(self):
        """Actualiza telefono"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        list_url = reverse("telefono-list")
        telefono = Telefono.objects.first()
        url = reverse("telefono-detail", args=(telefono.id,))
        self.client.patch(
            url,
            {"nombre": "telefono_actualizado_test_7", "numero": "987654327"},
            format="json",
        )
        response = self.client.get(list_url, format="json")
        response_data = json.loads(response.content)
        self.assertIn(
            response_data["results"][0]["nombre"], "telefono_actualizado_test_7"
        )
