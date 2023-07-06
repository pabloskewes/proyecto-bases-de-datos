import requests


HOST = "http://localhost"
PORT = 8091


# TODO: Fix "-> requests.Response" to use dicts with the correct types
class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_request(self, endpoint: str, params: dict = None) -> requests.Response:
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def check_connection(self) -> bool:
        response = self.make_request("/")
        return True

    def get_servicios(self) -> requests.Response:
        return self.make_request("/servicios")

    def get_comunas(self, region: int) -> requests.Response:
        return self.make_request("/comunas", params={"region": region})

    def get_recorridos(
        self, from_region: int, from_comuna: str, to_region: int, to_comuna: str
    ) -> requests.Response:
        return self.make_request(
            "/recorridos",
            params={
                "from_region": from_region,
                "from_comuna": from_comuna,
                "to_region": to_region,
                "to_comuna": to_comuna,
            },
        )

    def get_detalle_ruta(
        self, region: int, folio: int, nombre_recorrido: str
    ) -> requests.Response:
        return self.make_request(
            "/detalle_ruta",
            params={
                "region": region,
                "folio": folio,
                "nombre_recorrido": nombre_recorrido,
            },
        )

    def get_vehicles(self, region: int, comuna: str, calle: str) -> requests.Response:
        return self.make_request(
            "/vehicles",
            params={
                "region": region,
                "comuna": comuna,
                "calle": calle,
            },
        )


client = Client(base_url=f"{HOST}:{PORT}")


def get_client() -> Client:
    """Get the client"""
    return client
