import json

from agenda.models import Persona, Tratamiento
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase


class PaisTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = ["users.yaml", "tratamiento.yaml", "persona.yaml"]

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_lista_personas_return_http_ok(self):
        """Listar personas devuelve http 200"""
        url = reverse("persona-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_personas_return_len_ok(self):
        """Crear persona"""
        url = reverse("persona-list")
        tratamiento = Tratamiento.objects.first()
        self.client.post(
            url,
            {
                "nombre": "nombre_test_4",
                "apellidos": "apellidos_test_4",
                "tratamiento": 1,
            },
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 4)

    def test_elimina_persona_return_len_ok(self):
        """Elimina persona"""
        list_url = reverse("persona-list")
        persona = Persona.objects.first()
        url = reverse("persona-detail", args=(persona.id,))
        self.client.delete(url)
        response = self.client.get(list_url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_persona_return_details_ok(self):
        """Actualiza persona"""
        list_url = reverse("persona-list")
        persona = Persona.objects.first()
        url = reverse("persona-detail", args=(persona.id,))
        self.client.patch(url, {"nombre": "nombre_actualizado_test_2"}, format="json")
        response = self.client.get(list_url, format="json")
        response_data = json.loads(response.content)["results"]
        self.assertEqual(response_data[0]["nombre"], "nombre_actualizado_test_2")
