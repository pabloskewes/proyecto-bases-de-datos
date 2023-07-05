from typing import List, Dict

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import get_db
from src.logger import get_logger


logger = get_logger()

logger.log("Starting API", tags=["MAIN"])
app = FastAPI()


@app.get("/")
def index() -> Dict[str, str]:
    return {"message": "Hello, world!"}


@app.get("/servicios_orm", response_model=List[schemas.Servicio])
def get_servicios_orm(db: Session = Depends(get_db)):
    servicios = crud.get_servicios_orm(db)
    return servicios


@app.get("/servicios", response_model=List[schemas.Servicio])
def get_servicios(db: Session = Depends(get_db)):
    servicios = crud.get_servicios(db)
    return servicios
