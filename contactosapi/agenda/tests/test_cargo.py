import json

from agenda.models import Cargo, Correo, Telefono
from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase


class CargoTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]
    fixtures = [
        "users.yaml",
        "tratamiento.yaml",
        "provincia.yaml",
        "persona.yaml",
        "pais.yaml",
        "colectivo.yaml",
        "subcolectivo.yaml",
        "cargo.yaml",
    ]

    # maxDiff = None

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_lista_cargos_return_http_ok(self):
        """Listar cargos devuelve http 200"""
        url = reverse("cargo-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cargo_return_len_ok(self):
        """Crear cargo"""
        url = reverse("cargo-list")
        self.client.post(
            url,
            {
                "persona": 1,
                "cargo": "cargo_test_4",
                "finalizado": False,
                "ciudad": "ciudad_test_4",
                "cod_postal": 10004,
                "direccion": "direccion_test_4",
                "provincia": 1,
                "pais": 1,
                "empresa": "empresa_test_4",
                "fecha_alta": "2021-07-1T11:00:00+00:00",
                "fecha_modificacion": "2021-07-1T11:00:00+00:00",
                "colectivo": 1,
                "subcolectivo": 1,
                "usuario_modificacion": 1,
                "notas": "notas test data 4",
                "telefonos": [],
                "correos": [],
            },
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 4)

    def test_elimina_cargo_return_len_ok(self):
        """Elimina cargo"""
        urlList = reverse("cargo-list")
        cargo = Cargo.objects.first()
        url = reverse("cargo-detail", args=(cargo.id,))
        self.client.delete(url)
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 2)

    def test_actualiza_cargo_return_details_ok(self):
        """Actualiza cargo"""
        cargo = Cargo.objects.get(pk=1)
        telefono = Telefono.objects.create(
            cargo=cargo, nombre="nombre_test_1", numero=927232321, nota="nota test 1"
        )
        correo = Correo.objects.create(
            cargo=cargo,
            nombre="nombre_test_correo",
            email="prueba@tests.es",
            nota="nota_test correo",
        )
        url = reverse("cargo-detail", args=(cargo.id,))
        urlList = reverse("cargo-list")
        self.client.patch(
            url,
            {
                "cargo": "cargo_actualizado_test_4",
                "provincia": 2,
                "finalizado": True,
                "fecha_cese": "2017-05-01",
                "empresa": "empresa_actualizado_test_4",
                "pais": 2,
            },
            format="json",
        )
        response = self.client.get(urlList, format="json")
        to_exclude = ["fecha_cese", "fecha_alta", "fecha_modificacion"]
        cargo_data = json.loads(response.content)["results"][0]
        response_data = {k: v for k, v in cargo_data.items() if k not in to_exclude}
        desired_result = {
            "id": 1,
            "cargo": "cargo_actualizado_test_4",
            "persona": 1,
            "finalizado": True,
            "ciudad": "ciudad_test_1",
            "cod_postal": "10001",
            "direccion": "direccion_test_1",
            "provincia": 2,
            "pais": 2,
            "empresa": "empresa_actualizado_test_4",
            "colectivo": 1,
            "subcolectivo": 1,
            "usuario_modificacion": 1,
            "notas": "notas_test_1",
            "telefonos": [
                telefono.id,
            ],
            "correos": [
                correo.id,
            ],
        }
        self.assertDictEqual(response_data, desired_result)

    def test_cargo_detail(self):
        cargo = Cargo.objects.get(pk=1)
        url = reverse("cargo-detail", args=(cargo.id,))
        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(cargo.empresa, response.data["empresa"])
        self.assertEqual(cargo.cargo, response.data["cargo"])
