import json

from agenda.models import (
    Cargo,
    Colectivo,
    Pais,
    Persona,
    Provincia,
    SubColectivo,
    Tratamiento,
)
from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase


class CargoTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("", include("contactosapi.urls"))]

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_lista_cargos_return_http_ok(self):
        """Listar cargos devuelve http 200"""
        url = reverse("cargo-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cargo_return_len_ok(self):
        """Crear cargo"""
        url = reverse("cargo-list")
        tratamiento = Tratamiento.objects.create(nombre="tratamiento_test_1")
        persona = Persona.objects.create(
            nombre="nombre_test_1",
            apellidos="apellidos_test_1",
            tratamiento=tratamiento,
        )
        provincia = Provincia.objects.create(nombre="provincia_test_1")
        pais = Pais.objects.create(nombre="pais_test_1")
        colectivo = Colectivo.objects.create(nombre="colectivo_testing_1")
        subcolectivo = SubColectivo.objects.create(
            nombre="subcolectivo_testing_1", colectivo=colectivo
        )
        self.client.post(
            url,
            {
                "persona": {
                    "id": persona.id,
                    "nombre": persona.nombre,
                    "apellidos": persona.apellidos,
                    "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
                },
                "cargo": "cargo_test_1",
                "finalizado": False,
                "ciudad": "ciudad_test_1",
                "codPostal": "10001",
                "direccion": "direccion_test_1",
                "provincia": {"id": provincia.id, "nombre": provincia.nombre},
                "pais": {"id": pais.id, "nombre": pais.nombre},
                "empresa": "empresa_test_1",
                "fechaCese": "",
                "colectivo": {"id": colectivo.id, "nombre": colectivo.nombre},
                "subcolectivo": subcolectivo.nombre,
                "usuario_modificacion": self.user.username,
                "notas": "notas test data 1",
            },
            format="json",
        )
        self.client.post(
            url,
            {
                "persona": {
                    "id": persona.id,
                    "nombre": persona.nombre,
                    "apellidos": persona.apellidos,
                    "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
                },
                "cargo": "cargo_test_2",
                "finalizado": False,
                "ciudad": "ciudad_test_2",
                "codPostal": "10001",
                "direccion": "direccion_test_2",
                "provincia": {"id": provincia.id, "nombre": provincia.nombre},
                "pais": {"id": pais.id, "nombre": pais.nombre},
                "empresa": "empresa_test_2",
                "fechaCese": "",
                "colectivo": {"id": colectivo.id, "nombre": colectivo.nombre},
                "subcolectivo": subcolectivo.nombre,
                "usuario_modificacion": self.user.username,
                "notas": "notas test data 2",
            },
            format="json",
        )
        self.client.post(
            url,
            {
                "persona": {
                    "id": persona.id,
                    "nombre": persona.nombre,
                    "apellidos": persona.apellidos,
                    "tratamiento": {"id": tratamiento.id, "nombre": tratamiento.nombre},
                },
                "cargo": "cargo_test_3",
                "finalizado": False,
                "ciudad": "ciudad_test_3",
                "codPostal": "10001",
                "direccion": "direccion_test_3",
                "provincia": {"id": provincia.id, "nombre": provincia.nombre},
                "pais": {"id": pais.id, "nombre": pais.nombre},
                "empresa": "empresa_test_3",
                "fechaCese": "",
                "colectivo": {"id": colectivo.id, "nombre": colectivo.nombre},
                "subcolectivo": subcolectivo.nombre,
                "usuario_modificacion": self.user.username,
                "notas": "notas test data 3",
            },
            format="json",
        )
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 3)

    def test_elimina_cargo_return_len_ok(self):
        """Elimina cargo"""
        urlList = reverse("cargo-list")
        tratamiento = Tratamiento.objects.create(nombre="tratamiento_test_1")
        persona = Persona.objects.create(
            nombre="nombre_test_1",
            apellidos="apellidos_test_1",
            tratamiento=tratamiento,
        )
        provincia = Provincia.objects.create(nombre="provincia_test_1")
        pais = Pais.objects.create(nombre="pais_test_1")
        colectivo = Colectivo.objects.create(nombre="colectivo_testing_1")
        subcolectivo = SubColectivo.objects.create(
            nombre="subcolectivo_testing_1", colectivo=colectivo
        )
        cargo = Cargo.objects.create(
            colectivo=colectivo,
            cargo="cargo_test_1",
            persona=persona,
            finalizado=False,
            cod_postal=10005,
            ciudad="ciudad_test_1",
            direccion="direccion_test_1",
            provincia=provincia,
            pais=pais,
            empresa="empresa_test_1",
            subcolectivo=subcolectivo,
            usuario_modificacion=self.user,
            notas="notas test 1",
        )
        Cargo.objects.create(
            colectivo=colectivo,
            cargo="cargo_test_2",
            persona=persona,
            finalizado=False,
            cod_postal=10005,
            ciudad="ciudad_test_2",
            direccion="direccion_test_2",
            provincia=provincia,
            pais=pais,
            empresa="empresa_test_2",
            subcolectivo=subcolectivo,
            usuario_modificacion=self.user,
            notas="notas test 2",
        )
        url = reverse("cargo-detail", args=(cargo.id,))
        self.client.delete(url)
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response_data["count"], 1)

    def test_actualiza_cargo_return_details_ok(self):
        """Actualiza cargo"""
        tratamiento = Tratamiento.objects.create(nombre="tratamiento_test_1")
        persona = Persona.objects.create(
            nombre="nombre_test_1",
            apellidos="apellidos_test_1",
            tratamiento=tratamiento,
        )
        provincia = Provincia.objects.create(nombre="provincia_test_1")
        provincia2 = Provincia.objects.create(nombre="provincia_test_2")
        pais = Pais.objects.create(nombre="pais_test_1")
        colectivo = Colectivo.objects.create(nombre="colectivo_testing_1")
        subcolectivo = SubColectivo.objects.create(
            nombre="subcolectivo_testing_1", colectivo=colectivo
        )
        cargo = Cargo.objects.create(
            colectivo=colectivo,
            cargo="cargo_test_1",
            persona=persona,
            finalizado=False,
            cod_postal=10005,
            ciudad="ciudad_test_1",
            direccion="direccion_test_1",
            provincia=provincia,
            pais=pais,
            empresa="empresa_test_1",
            subcolectivo=subcolectivo,
            usuario_modificacion=self.user,
            notas="notas test 1",
        )
        url = reverse("cargo-detail", args=(cargo.id,))
        urlList = reverse("cargo-list")
        self.client.patch(
            url,
            {
                "cargo": "cargo_actualizado_test_2",
                "provincia": provincia2.id,
            },
            format="json",
        )
        response = self.client.get(urlList, format="json")
        response_data = json.loads(response.content)
        print(response_data)
        self.assertEqual(
            response_data["results"][0]["cargo"], "cargo_actualizado_test_2"
        )
        self.assertEqual(response_data["results"][0]["provincia"], provincia2.id)
