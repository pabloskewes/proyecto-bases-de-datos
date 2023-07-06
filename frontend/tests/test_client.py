import unittest

from src.client import get_client


class TestClient(unittest.TestCase):
    def test_check_connection(self):
        client = get_client()
        response = client.check_connection()
        self.assertTrue(response)

    def test_get_servicios(self):
        client = get_client()
        servicios = client.get_servicios()
        self.assertTrue(len(servicios) > 0)
        self.assertTrue(
            servicios[0].keys()
            == {"folio", "region", "tipo_servicio", "flota", "nombre_responsable"}
        )
