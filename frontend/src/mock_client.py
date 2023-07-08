class MockClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def check_connection(self) -> bool:
        return True

    def get_servicios(self):
        return [
            {
                "folio": 1,
                "region": 1,
                "tipo_servicio": "Servicio 1",
                "flota": "Flota 1",
                "nombre_responsable": "Nombre 1",
            },
            {
                "folio": 2,
                "region": 2,
                "tipo_servicio": "Servicio 2",
                "flota": "Flota 2",
                "nombre_responsable": "Nombre 2",
            },
        ]

    def get_comunas(self, region: int):
        return {"comunas": [f"region_{region}_comuna_1", f"region_{region}_comuna_2"]}

    def get_recorridos(
        self, from_region: int, from_comuna: str, to_region: int, to_comuna: str
    ):
        return [
            {
                "nombre_recorrido": f"recorrido_{from_comuna}_{to_comuna}_1",
                "id_origen": 1,
                "id_destino": 2,
                "s_folio": 1,
                "s_region": 1,
            },
            {
                "nombre_recorrido": f"recorrido_{from_comuna}_{to_comuna}_2",
                "id_origen": 2,
                "id_destino": 3,
                "s_folio": 2,
                "s_region": 2,
            },
        ]

    def get_detalle_ruta(self, region: int, folio: int, nombre_recorrido: str):
        return {
            "ida": [
                {
                    "calle": f"recorrido_{nombre_recorrido}_ida_calle_1",
                    "orden": 1,
                },
                {
                    "calle": f"recorrido_{nombre_recorrido}_ida_calle_2",
                    "orden": 2,
                },
            ],
            "regreso": [
                {
                    "calle": f"recorrido_{nombre_recorrido}_regreso_calle_1",
                    "orden": 1,
                },
                {
                    "calle": f"recorrido_{nombre_recorrido}_regreso_calle_2",
                    "orden": 2,
                },
            ],
        }

    def get_vehicles(self, region: int, comuna: str, calle: str):
        return {
            "vehicles": [
                {
                    "nombre_responsable": f"vehicle_{comuna}_{calle}_1",
                    "patente": "patente_1",
                    "marca": "marca_1",
                    "modelo": "modelo_1",
                    "año_fabricacion": 2000,
                },
                {
                    "nombre_responsable": f"vehicle_{comuna}_{calle}_2",
                    "patente": "patente_2",
                    "marca": "marca_2",
                    "modelo": "modelo_2",
                    "año_fabricacion": 2001,
                },
            ]
        }


client = MockClient(base_url="")


def get_client() -> MockClient:
    """Get the client"""
    return client
