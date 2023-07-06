from typing import List
from pydantic import BaseModel, Field


class Servicio(BaseModel):
    folio: int
    region: int
    tipo_servicio: str
    flota: int
    nombre_responsable: str


class ComunaQueryParams(BaseModel):
    region: int = Field(..., ge=1, le=16)


class ComunaResponse(BaseModel):
    comunas: List[str]


class Recorrido(BaseModel):
    nombre_recorrido: str
    id_origen: int
    id_destino: int
    s_folio: int
    s_region: int


class BusquedaRecorridoQueryParams(BaseModel):
    from_region: int
    to_region: int
    from_comuna: str
    to_comuna: str


class BusquedaRecorridoResponse(BaseModel):
    recorridos: List[Recorrido]


class Calle(BaseModel):
    calle: str
    orden: int


class DetalleRutaQueryParams(BaseModel):
    region: int
    folio: int
    nombre_recorrido: str


class DetalleRutaResponse(BaseModel):
    ida: List[Calle]
    regreso: List[Calle]


class VehicleQueryParams(BaseModel):
    region: int
    comuna: str
    calle: str


class VehicleResponse(BaseModel):
    nombre_responsable: str
    patente: str
    marca: str
    modelo: str
    año_fabricacion: int
