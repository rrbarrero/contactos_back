import json
from django.contrib.auth.models import User
from django.urls import include, reverse, path
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, URLPatternsTestCase
from agenda.models import Persona, Tratamiento


class PaisTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_lista_personas_return_http_ok(self):
        """Listar personas devuelve http 200"""
        url = reverse("persona-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_personas_return_len_ok(self):
        """Crear persona"""
        url = reverse("persona-list")
        tratamiento = Tratamiento.objects.create(nombre="tratamiento_test_1")
        self.client.post(
            url,
            {
                "nombre": "nombre_test_1",
                "apellidos": "apellidos_test_1",
                "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
            },
            format="json",
        )
        self.client.post(
            url,
            {
                "nombre": "nombre_test_2",
                "apellidos": "apellidos_test_2",
                "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
            },
            format="json",
        )
        self.client.post(
            url,
            {
                "nombre": "nombre_test_3",
                "apellidos": "apellidos_test_3",
                "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
            },
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 3)

    def test_elimina_persona_return_len_ok(self):
        """Elimina persona"""
        urlList = reverse("persona-list")
        tratamiento = Tratamiento.objects.create(nombre="tratamiento_test_1")
        self.client.post(
            urlList,
            {
                "nombre": "nombre_test_1",
                "apellidos": "apellidos_test_1",
                "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
            },
            format="json",
        )
        self.client.post(
            urlList,
            {
                "nombre": "nombre_test_2",
                "apellidos": "apellidos_test_2",
                "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
            },
            format="json",
        )
        self.client.post(
            urlList,
            {
                "nombre": "nombre_test_3",
                "apellidos": "apellidos_test_3",
                "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
            },
            format="json",
        )
        persona = Persona.objects.first()
        url = reverse("persona-detail", args=(persona.id,))
        self.client.delete(url)
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)

    def test_actualiza_persona_return_details_ok(self):
        """Actualiza persona"""
        url = reverse("persona-detail", args=(1,))
        urlList = reverse("persona-list")
        tratamiento = Tratamiento.objects.create(nombre="tratamiento_test_1")
        self.client.post(
            urlList,
            {
                "nombre": "nombre_test_2",
                "apellidos": "apellidos_test_2",
                "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
            },
            format="json",
        )
        self.client.patch(url, {"nombre": "nombre_actualizado_test_2"}, format="json")
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]["nombre"], "nombre_actualizado_test_2")
