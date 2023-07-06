from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src import schemas, crud
from src.database import get_db

router = APIRouter()


@router.get("/")
def index() -> Dict[str, str]:
    return {"message": "Hello, world!"}


@router.get("/servicios_orm", response_model=List[schemas.Servicio])
def get_servicios_orm(db: Session = Depends(get_db)):
    servicios = crud.get_servicios_orm(db)
    return servicios


@router.get("/servicios", response_model=List[schemas.Servicio])
def get_servicios(db: Session = Depends(get_db)):
    servicios = crud.get_servicios(db)
    return servicios


@router.get("/recorridos", response_model=List[schemas.Recorrido])
def get_recorridos(
    db: Session = Depends(get_db),
    params: schemas.BusquedaRecorridoQueryParams = Depends(),
):
    recorridos = crud.get_recorridos(db, params)
    return recorridos


@router.get("/detalle_ruta", response_model=schemas.DetalleRutaResponse)
def get_detalle_ruta(
    db: Session = Depends(get_db), params: schemas.DetalleRutaQueryParams = Depends()
):
    detalle_ruta = crud.get_detalle_ruta(db, params)
    return detalle_ruta


@router.get("/vehicles", response_model=List[schemas.VehicleResponse])
def get_vehicles(
    db: Session = Depends(get_db), params: schemas.VehicleQueryParams = Depends()
):
    vehicles = crud.get_vehicles(db, params)
    return vehicles


@router.get("/comunas", response_model=List[str])
def get_comunas(db: Session = Depends(get_db), params: dict[int] = {}):
    comunas = crud.get_vehicles(db, params)
    return comunas
