import json

from agenda.models import Provincia
from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase


class ProvinciaTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = ["users.yaml", "provincia.yaml"]

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_lista_provincias_return_http_ok(self):
        """Listar provincias devuelve http 200"""
        url = reverse("provincia-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_provincia_return_len_ok(self):
        """Crear provincia"""
        url = reverse("provincia-list")
        self.client.post(
            url,
            {"nombre": "provincia_test_4"},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "provincia_test_5"},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "provincia_test_6"},
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 6)

    def test_elimina_provincia_return_len_ok(self):
        """Elimina provincia"""
        urlList = reverse("provincia-list")
        provincia = Provincia.objects.first()
        url = reverse("provincia-detail", args=(provincia.id,))
        self.client.delete(url)
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_un_provincia_return_details_ok(self):
        """Actualiza provincia"""
        urlList = reverse("provincia-list")
        provincia = Provincia.objects.first()
        url = reverse("provincia-detail", args=(provincia.id,))
        self.client.patch(
            url, {"nombre": "provincia_actualizado_test_2"}, format="json"
        )
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertIn(
            response_data["results"][0]["nombre"], "provincia_actualizado_test_2"
        )
