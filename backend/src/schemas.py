from pydantic import BaseModel


class Servicio(BaseModel):
    folio: int
    region: int
    tipo_servicio: str
    flota: int
    nombre_responsable: str


class Lugar(BaseModel):
    id: int
    nombre: str
    comuna: str
    domicilio: str


class Trazado(BaseModel):
    sentido: str
    calle: str
    comuna: str


class Vehiculo(BaseModel):
    patente: str
    s_folio: int
    s_region: int
    marca: str
    fecha_ingreso: str
    capacidad: int
    año_fabricacion: int
    modelo: str
    tipo_servicio: str


class Recorrido(BaseModel):
    nombre_recorrido: str
    id_origen: int
    id_destino: int
    s_folio: int
    s_region: int


class PasaPor(BaseModel):
    r_nombre_recorrido: str
    r_calle: str
    t_comuna: str
    t_sentido: str
    orden: int
    s_folio: int
    s_region: int
