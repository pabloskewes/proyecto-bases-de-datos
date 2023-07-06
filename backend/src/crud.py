from typing import List, Dict

from sqlalchemy.orm import Session
from sqlalchemy import text

from src import models, schemas


def exec_raw_query(db: Session, raw_query: str, params: Dict[str, any] = None) -> List[Dict]:
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


def get_comunas(db: Session, region: int) -> List[str]:
    raw_query = f"""
    SELECT * FROM comunasregion{region};
    """
    params = {"region": region}
    return exec_raw_query(db, raw_query, params)


def get_recorridos(db: Session, from_region: int, to_region: int, from_comuna: str, to_comuna: str) -> List[Dict]:
    raw_query = """
    SELECT * FROM recorrido 
    WHERE id_origen IN (
        SELECT id FROM lugar L1
        WHERE L1.region = :from_region AND L1.comuna LIKE :from_comuna
        )
    AND id_destino IN (           
        SELECT id FROM lugar L2
        WHERE L2.region = :to_region AND L2.comuna LIKE :to_comuna
        );

    """
    params = {"from_region": from_region, "to_region": to_region,   "from_comuna": from_comuna, "to_comuna": to_comuna}
    return exec_raw_query(db, raw_query, params)


# TODO: FIX QUERY
def get_detalle_ruta(db: Session, region: int, folio: int, nombre_recorrido: str) -> List[Dict]:
    raw_query = """
    SELECT * FROM pasapor 
    WHERE s_region = :region
    AND s_folio = :folio
    AND r_nombre_recorrido LIKE :nombre_recorrido
    ORDER BY t_sentido, orden;
    """
    params = {"region": region, "folio": folio, "nombre_recorrido": nombre_recorrido}
    results = exec_raw_query(db, raw_query, params)

    ida, regreso = [], []
    for trazado in results:
        if trazado['t_sentido'] == 'IDA':
            ida.append(trazado)
        else:
            regreso.append(trazado)
    return {"ida": ida, "regreso": regreso}


# TODO: FIX QUERY
def get_vehicles(db: Session, region: int, comuna: str, calle: str) -> List[Dict]:
    raw_query = """
    SELECT patente, marca, modelo, anho_fabricacion AS año_fabricacion FROM vehiculo V
    WHERE V.s_region = :region AND V.s_folio IN (
        SELECT P.s_folio FROM pasapor P
        WHERE P.s_region = :region AND P.t_calle LIKE :calle AND P.t_comuna LIKE :comuna);
    """
    params = {"region": region, "comuna": comuna, "calle": calle}
    return exec_raw_query(db, raw_query, params)
