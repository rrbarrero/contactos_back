import json
from django.contrib.auth.models import User
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase
from agenda.models import Colectivo


class ColectivosTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        # token = Token.objects.get(user__username='testuser')
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_lista_colectivos_return_http_ok(self):
        """Listar colectivos devuelve http 200"""
        url = reverse("colectivo-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crea_colectivos_return_http_created_1(self):
        """Crea colectivos"""
        nuevo_colectivo = {"nombre": "colectivo_test_1"}
        url = reverse("colectivo-list")
        response = self.client.post(url, nuevo_colectivo, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crea_colectivos_return_len_ok(self):
        """Lista los Colectivos"""
        url = reverse("colectivo-list")
        self.client.post(url, {"nombre": "colectivo_test_1"}, format="json")
        self.client.post(url, {"nombre": "colectivo_test_2"}, format="json")
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_elimina_colectivo_return_len_ok(self):
        """Elimina Colectivos"""
        urlList = reverse("colectivo-list")
        self.client.post(urlList, {"nombre": "colectivo_test_1"}, format="json")
        self.client.post(urlList, {"nombre": "colectivo_test_2"}, format="json")
        self.client.post(urlList, {"nombre": "colectivo_test_3"}, format="json")
        colectivo = Colectivo.objects.first()
        url = reverse("colectivo-detail", args=(colectivo.id,))
        self.client.delete(url)
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_un_colectivo_return_details_ok(self):
        """Actualiza Colectivos"""
        url = reverse("colectivo-detail", args=(1,))
        urlList = reverse("colectivo-list")
        self.client.post(urlList, {"nombre": "colectivo_test_1"}, format="json")
        self.client.patch(
            url, {"nombre": "colectivo_actualizado_test_2"}, format="json"
        )
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertIn(
            response_data["results"][0]["nombre"], "colectivo_actualizado_test_2"
        )
