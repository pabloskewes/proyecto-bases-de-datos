from typing import List
from pydantic import BaseModel, Field


class Servicio(BaseModel):
    folio: int
    region: int
    tipo_servicio: str
    flota: int
    nombre_responsable: str


class Recorrido(BaseModel):
    nombre_recorrido: str
    lugar_origen: str
    lugar_destino: str
    s_folio: int
    s_region: int


class Trazado(BaseModel):
    region: int
    calle: str
    comuna: str
    orden: int


class ComunaQueryParams(BaseModel):
    region: int = Field(..., ge=1, le=16)


class ComunaResponse(BaseModel):
    comunas: List[str]


class BusquedaRecorridoQueryParams(BaseModel):
    from_region: int
    to_region: int
    from_comuna: str
    to_comuna: str


class BusquedaRecorridoResponse(BaseModel):
    recorridos: List[Recorrido]


class DetalleRutaQueryParams(BaseModel):
    region: int
    folio: int
    nombre_recorrido: str


class DetalleRutaResponse(BaseModel):
    ida: List[Trazado]
    regreso: List[Trazado]


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
