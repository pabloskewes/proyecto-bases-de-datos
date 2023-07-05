from typing import List, Dict

from sqlalchemy.orm import Session
from sqlalchemy import text

from src import models, schemas


def exec_raw_query(db: Session, raw_query: str) -> List[Dict]:
    """
    Execute a raw query and return the result as a list of dictionaries
    Args:
        db (Session): SQLAlchemy session
        raw_query (str): Raw query to execute

    """
    result = db.execute(text(raw_query))
    rows = result.fetchall()
    columns = result.keys()

    return [dict(zip(columns, row)) for row in rows]


# TODO: No funcionan los modelos con ORM porque el esquema no está bien
# No sé si hay que arreglar el models.py o la base de datos
def get_servicios_orm(db: Session):
    return db.query(models.Servicio).all()


def get_servicios(db: Session) -> List[Dict]:
    raw_query = """
    SELECT * FROM servicio LIMIT 10;
    """
    return exec_raw_query(db, raw_query)
