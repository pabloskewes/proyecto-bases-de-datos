from typing import List, Dict, Any
import requests

from src.dto import (
    ServicioDTO,
    ComunaDTO,
    RecorridoDTO,
    CalleDTO,
    DetalleRutaDTO,
    VehicleDTO,
)

HOST = "http://localhost"
PORT = 8091


def map_servicios(response: List[dict]) -> List[ServicioDTO]:
    return [ServicioDTO(**item) for item in response]


def map_comunas(response: dict) -> List[ComunaDTO]:
    return [ComunaDTO(nombre=comuna) for comuna in response["comunas"]]


def map_recorridos(response: Dict[str, List[RecorridoDTO]]) -> List[RecorridoDTO]:
    return [RecorridoDTO(**item) for item in response["recorridos"]]


def map_detalle_ruta(response: dict) -> DetalleRutaDTO:
    ida = [
        CalleDTO(nombre=calle["calle"], orden=calle["orden"])
        for calle in response["ida"]
    ]
    regreso = [
        CalleDTO(nombre=calle["calle"], orden=calle["orden"])
        for calle in response["regreso"]
    ]
    return DetalleRutaDTO(ida=ida, regreso=regreso)


def map_vehicles(response: dict) -> List[VehicleDTO]:
    return [VehicleDTO(**item) for item in response["vehicles"]]


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_request(self, endpoint: str, params: dict = None) -> Dict[str, Any]:
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def check_connection(self) -> bool:
        self.make_request("/")
        return True

    def get_servicios(self) -> requests.Response:
        response = self.make_request("/servicios")
        return map_servicios(response)

    def get_comunas(self, region: int) -> List[str]:
        response = self.make_request("/comunas", params={"region": region})
        return map_comunas(response)

    def get_recorridos(
        self, from_region: int, from_comuna: str, to_region: int, to_comuna: str
    ) -> List[RecorridoDTO]:
        response = self.make_request(
            "/recorridos",
            params={
                "from_region": from_region,
                "from_comuna": from_comuna,
                "to_region": to_region,
                "to_comuna": to_comuna,
            },
        )
        return map_recorridos(response)

    def get_detalle_ruta(
        self, region: int, folio: int, nombre_recorrido: str
    ) -> DetalleRutaDTO:
        response = self.make_request(
            "/detalle_ruta",
            params={
                "region": region,
                "folio": folio,
                "nombre_recorrido": nombre_recorrido,
            },
        )
        return map_detalle_ruta(response)

    def get_vehicles(self, region: int, comuna: str, calle: str) -> List[VehicleDTO]:
        response = self.make_request(
            "/vehicles",
            params={
                "region": region,
                "comuna": comuna,
                "calle": calle,
            },
        )
        return map_vehicles(response)


client = Client(base_url=f"{HOST}:{PORT}")


def get_client() -> Client:
    """Get the client"""
    return client
