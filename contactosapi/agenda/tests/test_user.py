import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase


class UserTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = ["users.yaml"]

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def test_usuario_puede_logarse_y_obtener_token(self):
        url = reverse("user-login")
        token = Token.objects.get(user=self.user)
        response = self.client.post(
            url, {"username": "testuser", "password": "12345"}, format="json"
        )
        data = json.loads(response.content)
        self.assertEqual(data["token"], token.key)

    def test_usuario_puede_usar_su_token(self):
        url = reverse("user-login")
        response = self.client.post(
            url, {"username": "testuser", "password": "12345"}, format="json"
        )
        data = json.loads(response.content)
        token = data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(reverse("colectivo-list"))
        self.assertEqual(response.status_code, 200)

    def test_usuario_sin_token_no_puede_consultar(self):
        response = self.client.get(reverse("colectivo-list"))
        self.assertEqual(response.status_code, 403)

    def test_busca_sin_login_no_esta_permitido(self):
        url = reverse("busca-contacto")
        response = self.client.get(
            url,
            {"termino1": "nombre_test_3", "termino2": "apellidos_test_3"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)
