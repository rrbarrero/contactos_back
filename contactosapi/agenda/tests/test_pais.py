import json
from django.contrib.auth.models import User
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase
from agenda.models import Pais


class PaisTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = ["users.yaml", "pais.yaml"]

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_lista_paises_return_http_ok(self):
        """Listar paises devuelve http 200"""
        url = reverse("pais-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_pais_return_len_ok(self):
        """Crear país"""
        url = reverse("pais-list")
        self.client.post(
            url,
            {"nombre": "pais_test_4"},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "pais_test_5"},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "pais_test_6"},
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 6)

    def test_elimina_pais_return_len_ok(self):
        """Elimina país"""
        urlList = reverse("pais-list")
        pais = Pais.objects.first()
        url = reverse("pais-detail", args=(pais.id,))
        self.client.delete(url)
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_un_pais_return_details_ok(self):
        """Actualiza país"""
        urlList = reverse("pais-list")
        pais = Pais.objects.first()
        url = reverse("pais-detail", args=(pais.id,))
        self.client.patch(url, {"nombre": "pais_actualizado_test_2"}, format="json")
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertIn(response_data["results"][0]["nombre"], "pais_actualizado_test_2")
