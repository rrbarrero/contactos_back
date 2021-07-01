import json
from django.contrib.auth.models import User
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase
from agenda.models import Tratamiento


class TratamientoTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = ["users.yaml", "tratamiento.yaml"]

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_lista_tratamientos_return_http_ok(self):
        """Listar tratamientos devuelve http 200"""
        url = reverse("tratamiento-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tratamiento_return_len_ok(self):
        """Crear tratamiento"""
        url = reverse("tratamiento-list")
        self.client.post(
            url,
            {"nombre": "tratamiento_test_4"},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "tratamiento_test_5"},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "tratamiento_test_6"},
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 6)

    def test_elimina_tratamiento_return_len_ok(self):
        """Elimina tratamiento"""
        urlList = reverse("tratamiento-list")
        tratamiento = Tratamiento.objects.first()
        url = reverse("tratamiento-detail", args=(tratamiento.id,))
        self.client.delete(url)
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_un_tratamiento_return_details_ok(self):
        """Actualiza tratamiento"""
        urlList = reverse("tratamiento-list")
        tratamiento = Tratamiento.objects.first()
        url = reverse("tratamiento-detail", args=(tratamiento.id,))
        self.client.patch(
            url, {"nombre": "tratamiento_actualizado_test_2"}, format="json"
        )
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertIn(
            response_data["results"][0]["nombre"], "tratamiento_actualizado_test_2"
        )
