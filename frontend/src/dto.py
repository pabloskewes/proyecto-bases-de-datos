from typing import List
from pydantic import BaseModel


class ServicioDTO(BaseModel):
    folio: int
    region: int
    tipo_servicio: str
    flota: str
    nombre_responsable: str


class ComunaDTO(BaseModel):
    nombre: str


class RecorridoDTO(BaseModel):
    nombre_recorrido: str
    lugar_origen: str
    lugar_destino: str
    s_folio: int
    s_region: int


class CalleDTO(BaseModel):
    nombre: str
    orden: int


class DetalleRutaDTO(BaseModel):
    ida: List[CalleDTO]
    regreso: List[CalleDTO]


class VehicleDTO(BaseModel):
    nombre_responsable: str
    patente: str
    marca: str
    modelo: str
    año_fabricacion: int
