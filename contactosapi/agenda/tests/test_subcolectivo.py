import json
from django.contrib.auth.models import User
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase
from agenda.models import Colectivo, SubColectivo


class SubcolectivosTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_lista_subcolectivos_return_http_ok(self):
        """Listar colectivos devuelve http 200"""
        url = reverse("subcolectivo-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_subcolectivos_return_len_ok(self):
        """Crear subcolectivos"""
        colectivo = Colectivo.objects.create(nombre="colectivo_testing_1")
        url = reverse("subcolectivo-list")
        self.client.post(
            url,
            {"nombre": "subcolectivo_test_1", "colectivo": colectivo.id},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "subcolectivo_test_2", "colectivo": colectivo.id},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "subcolectivo_test_3", "colectivo": colectivo.id},
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 3)

    def test_elimina_subcolectivo_return_len_ok(self):
        """Elimina Colectivos"""
        colectivo = Colectivo.objects.create(nombre="colectivo_testing_1")
        urlList = reverse("subcolectivo-list")
        self.client.post(
            urlList,
            {"nombre": "colectivo_test_1", "colectivo": colectivo.id},
            format="json",
        )
        self.client.post(
            urlList,
            {"nombre": "colectivo_test_2", "colectivo": colectivo.id},
            format="json",
        )
        self.client.post(
            urlList,
            {"nombre": "colectivo_test_3", "colectivo": colectivo.id},
            format="json",
        )
        subcolectivo = SubColectivo.objects.first()
        url = reverse("subcolectivo-detail", args=(subcolectivo.id,))
        self.client.delete(url)
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_un_subcolectivo_return_details_ok(self):
        """Actualiza SubColectivos"""
        colectivo = Colectivo.objects.create(nombre="colectivo_test_1")
        subcolectivo = SubColectivo.objects.create(
            nombre="subcolectivo_test_1", colectivo=colectivo
        )
        url = reverse("subcolectivo-detail", args=(subcolectivo.id,))
        urlList = reverse("subcolectivo-list")
        self.client.patch(
            url, {"nombre": "subcolectivo_actualizado_test_2"}, format="json"
        )
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertIn(
            response_data["results"][0]["nombre"], "subcolectivo_actualizado_test_2"
        )
