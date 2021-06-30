import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase


class UserTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        # self.client.login(username="testuser", password="12345")

    def test_usuario_puede_logarse_y_obtener_token(self):
        url = reverse("user-login")
        token = Token.objects.get(user=self.user)
        response = self.client.post(
            url, {"username": "testuser", "password": "12345"}, format="json"
        )
        data = json.loads(response.content)
        assert data["token"] == token.key

    def test_usuario_puede_usar_su_token(self):
        url = reverse("user-login")
        response = self.client.post(
            url, {"username": "testuser", "password": "12345"}, format="json"
        )
        data = json.loads(response.content)
        token = data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(reverse("colectivo-list"))
        assert response.status_code == 200

    def test_usuario_sin_token_no_puede_consultar(self):
        response = self.client.get(reverse("colectivo-list"))
        assert response.status_code == 403
