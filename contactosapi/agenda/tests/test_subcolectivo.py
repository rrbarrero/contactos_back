import json
from django.conf import settings
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase
from agenda.models import Colectivo, SubColectivo


class SubcolectivosTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = ["colectivo.yaml", "subcolectivo.yaml"]

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

    def test_lista_subcolectivos_return_http_ok(self):
        """Listar colectivos devuelve http 200"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("subcolectivo-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_subcolectivos_return_len_ok(self):
        """Crear subcolectivos"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        colectivo = Colectivo.objects.create(nombre="colectivo_testing_1")
        url = reverse("subcolectivo-list")
        self.client.post(
            url,
            {"nombre": "subcolectivo_test_4", "colectivo": colectivo.id},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "subcolectivo_test_5", "colectivo": colectivo.id},
            format="json",
        )
        self.client.post(
            url,
            {"nombre": "subcolectivo_test_6", "colectivo": colectivo.id},
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 6)

    def test_elimina_subcolectivo_return_len_ok(self):
        """Elimina Colectivos"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        colectivo = Colectivo.objects.first()
        list_url = reverse("subcolectivo-list")
        subcolectivo = SubColectivo.objects.first()
        url = reverse("subcolectivo-detail", args=(subcolectivo.id,))
        self.client.delete(url)
        response = self.client.get(list_url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_un_subcolectivo_return_details_ok(self):
        """Actualiza SubColectivos"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        colectivo = Colectivo.objects.first()
        subcolectivo = SubColectivo.objects.first()
        url = reverse("subcolectivo-detail", args=(subcolectivo.id,))
        list_url = reverse("subcolectivo-list")
        self.client.patch(
            url, {"nombre": "subcolectivo_actualizado_test_2"}, format="json"
        )
        response = self.client.get(list_url, format="json")
        response_data = json.loads(response.content)
        self.assertIn(
            response_data["results"][0]["nombre"], "subcolectivo_actualizado_test_2"
        )
