import json
from django.conf import settings
from visago.models import CustomUser as User
from rest_framework.authtoken.models import Token
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase


class UserTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    # fixtures = ["users.yaml"]

    # def setUp(self):
    #     self.user = User.objects.get(pk=1)

    def test_usuario_invalido_no_puede_logarse(self):
        url = reverse("auth-login")
        response = self.client.post(
            url, {"username": "testuser", "password": "12345"}, format="json"
        )
        data = json.loads(response.content)
        self.assertEqual(data["detail"], "Invalid login")

    def test_usuario_valido_puede_logarse_y_obtener_un_token(self):
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
        self.assertEqual(data["response"], "login_success")

    def test_usuario_puede_usar_su_token(self):
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
        token = data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
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
