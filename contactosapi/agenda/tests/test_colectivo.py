import json
from django.conf import settings
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase
from agenda.models import Colectivo


class ColectivosTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = ["colectivo.yaml"]

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

    def test_lista_colectivos_return_http_ok(self):
        """Listar colectivos devuelve http 200"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("colectivo-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crea_colectivos_return_http_created_1(self):
        """Crea colectivos"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        nuevo_colectivo = {"nombre": "colectivo_test_4"}
        url = reverse("colectivo-list")
        response = self.client.post(url, nuevo_colectivo, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crea_colectivos_return_len_ok(self):
        """Lista los Colectivos"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        url = reverse("colectivo-list")
        self.client.post(url, {"nombre": "colectivo_test_4"}, format="json")
        self.client.post(url, {"nombre": "colectivo_test_5"}, format="json")
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 5)

    def test_elimina_colectivo_return_len_ok(self):
        """Elimina Colectivos"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        list_url = reverse("colectivo-list")
        colectivo = Colectivo.objects.first()
        url = reverse("colectivo-detail", args=(colectivo.id,))
        self.client.delete(url)
        response = self.client.get(list_url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_un_colectivo_return_details_ok(self):
        """Actualiza Colectivos"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        list_url = reverse("colectivo-list")
        colectivo = Colectivo.objects.first()
        url = reverse("colectivo-detail", args=(colectivo.id,))
        self.client.patch(
            url, {"nombre": "colectivo_actualizado_test_2"}, format="json"
        )
        response = self.client.get(list_url, format="json")
        response_data = json.loads(response.content)
        self.assertIn(
            response_data["results"][0]["nombre"], "colectivo_actualizado_test_2"
        )
