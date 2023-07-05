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
