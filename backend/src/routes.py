from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src import schemas, crud
from src.database import get_db

router = APIRouter()


@router.get("/")
def index() -> Dict[str, str]:
    return {"message": "Hello, world!"}


@router.get("/servicios", response_model=List[schemas.Servicio])
def get_servicios(db: Session = Depends(get_db)):
    servicios = crud.get_servicios(db)
    return servicios


@router.get("/comunas", response_model=schemas.ComunaResponse)
def get_comunas(
    db: Session = Depends(get_db), params: schemas.ComunaQueryParams = Depends()
):
    comunas = crud.get_comunas(db, params)
    return comunas


@router.get("/recorridos", response_model=schemas.BusquedaRecorridoResponse)
def get_recorridos(
    db: Session = Depends(get_db),
    params: schemas.BusquedaRecorridoQueryParams = Depends(),
):
    recorridos = crud.get_recorridos(db=db, **params.dict())
    return recorridos


@router.get("/detalle_ruta", response_model=schemas.DetalleRutaResponse)
def get_detalle_ruta(
    db: Session = Depends(get_db), params: schemas.DetalleRutaQueryParams = Depends()
):
    detalle_ruta = crud.get_detalle_ruta(db, **params.dict())
    return detalle_ruta


@router.get("/vehicles", response_model=List[schemas.VehicleResponse])
def get_vehicles(
    db: Session = Depends(get_db), params: schemas.VehicleQueryParams = Depends()
):
    vehicles = crud.get_vehicles(db, **params.dict())
    return vehicles


@router.get("/localization", response_model=schemas.LocalizationResponse)
def get_localization(
    db: Session = Depends(get_db), params: schemas.LocalizationQueryParams = Depends()
):
    localization = crud.get_localization(db, **params.dict())
    return localization
