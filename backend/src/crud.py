from typing import List, Dict

from sqlalchemy.orm import Session
from sqlalchemy import text

from src import models, schemas


def exec_raw_query(
    db: Session, raw_query: str, params: Dict[str, any] = None
) -> List[Dict]:
    """
    Execute a raw query with parameters and return the result as a list of dictionaries
    Args:
        db (Session): SQLAlchemy session
        raw_query (str): Raw query to execute
        params (Dict[str, any]): Parameters for the query

    """
    result = db.execute(text(raw_query), params)
    rows = result.fetchall()
    columns = result.keys()

    return [dict(zip(columns, row)) for row in rows]


def get_servicios(db: Session) -> List[Dict]:
    raw_query = """
    SELECT * FROM servicio LIMIT 10;
    """
    return exec_raw_query(db, raw_query)
