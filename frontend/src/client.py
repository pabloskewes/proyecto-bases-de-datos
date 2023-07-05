import requests


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_request(self, endpoint: str) -> requests.Response:
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def check_connection(self) -> bool:
        response = self.make_request("/")
        return True

    def get_servicios(self) -> requests.Response:
        return self.make_request("/servicios")


def get_client() -> Client:
    host = "http://localhost"
    port = 8091
    return Client(base_url=f"{host}:{port}")
