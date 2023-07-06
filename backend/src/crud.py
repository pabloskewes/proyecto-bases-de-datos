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


# TODO: FIX QUERY
def get_recorridos(
    db: Session, region: int, from_comuna: str, to_comuna: str
) -> List[Dict]:
    raw_query = """
    SELECT * FROM recorrido WHERE s_region = :region AND id_origen = (SELECT id FROM lugar WHERE comuna = :from_comuna) AND id_destino = (SELECT id FROM lugar WHERE comuna = :to_comuna);
    """
    params = {"region": region, "from_comuna": from_comuna, "to_comuna": to_comuna}
    return exec_raw_query(db, raw_query, params)


# TODO: FIX QUERY
def get_detalle_ruta(
    db: Session, region: int, folio: int, nombre_recorrido: str
) -> List[Dict]:
    raw_query = """
    SELECT * FROM trazado WHERE sentido = 'ida' AND comuna IN (SELECT comuna FROM recorrido WHERE s_region = :region AND s_folio = :folio AND nombre_recorrido = :nombre_recorrido) ORDER BY orden;
    """
    params = {"region": region, "folio": folio, "nombre_recorrido": nombre_recorrido}
    ida = exec_raw_query(db, raw_query, params)

    raw_query = """
    SELECT * FROM trazado WHERE sentido = 'regreso' AND comuna IN (SELECT comuna FROM recorrido WHERE s_region = :region AND s_folio = :folio AND nombre_recorrido = :nombre_recorrido) ORDER BY orden;
    """
    params = {"region": region, "folio": folio, "nombre_recorrido": nombre_recorrido}
    regreso = exec_raw_query(db, raw_query, params)

    return {"ida": ida, "regreso": regreso}


# TODO: FIX QUERY
def get_vehicles(db: Session, region: int, comuna: str, calle: str) -> List[Dict]:
    raw_query = """
    SELECT * FROM vehiculo WHERE region = :region AND comuna = :comuna AND calle = :calle;
    """
    params = {"region": region, "comuna": comuna, "calle": calle}
    return exec_raw_query(db, raw_query, params)
