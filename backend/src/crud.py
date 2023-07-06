from typing import List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import text

from src.logger import get_logger


logger = get_logger()


@logger.wrap_func(tags=["CRUD"])
def exec_raw_query(db: Session, raw_query: str, params: Dict[str, any] = None) -> Any:
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
    logger.log(f"{rows = }")
    logger.log(f"{columns = }")
    records = [dict(zip(columns, row)) for row in rows]

    logger.log("Performed following query:")
    logger.log(raw_query)
    logger.log("With parameters:")
    logger.log(params)
    logger.log(f"Got {len(records)} results")
    logger.log("Results:")
    logger.log(records)

    return records


def get_servicios(db: Session) -> List[Dict]:
    raw_query = """
    SELECT * FROM servicio LIMIT 10;
    """
    return exec_raw_query(db, raw_query)


def get_comunas(db: Session, region: int) -> List[str]:
    int_region = int(str(region).split("=")[-1])
    raw_query = f"""
    SELECT * FROM comunasregion{int_region};
    """
    params = {"region": region}
    records = exec_raw_query(db, raw_query, params)
    results = [record["comuna"] for record in records]
    return {"comunas": results}


def get_recorridos(
    db: Session, from_region: int, to_region: int, from_comuna: str, to_comuna: str
) -> List[Dict]:
    raw_query = """
    SELECT R.nombre_recorrido AS nombre_recorrido, R.s_region AS s_region, R.s_folio, L1.nombre AS lugar_origen, L2.nombre AS lugar_destino FROM recorrido R, lugar L1, lugar L2
    WHERE (R.id_origen = L1.id AND L1.region = :from_region AND L1.comuna LIKE :from_comuna)
    AND (R.id_destino = L2.id AND L2.region = :to_region AND L2.comuna LIKE :to_comuna);

    """
    params = {
        "from_region": from_region,
        "to_region": to_region,
        "from_comuna": from_comuna,
        "to_comuna": to_comuna,
    }
    results = exec_raw_query(db, raw_query, params)
    return results


def get_detalle_ruta(
    db: Session, region: int, folio: int, nombre_recorrido: str
) -> List[Dict]:
    raw_query = """
    SELECT t_calle AS calle, orden, t_sentido FROM pasapor 
    WHERE s_region = :region
    AND s_folio = :folio
    AND r_nombre_recorrido LIKE :nombre_recorrido
    ORDER BY t_sentido, orden;
    """
    params = {"region": region, "folio": folio, "nombre_recorrido": nombre_recorrido}
    results = exec_raw_query(db, raw_query, params)

    ida, regreso = [], []
    for trazado in results:
        new_trazado = {key: trazado[key] for key in ["calle", "orden"]}
        if trazado["t_sentido"] == "IDA":
            ida.append(new_trazado)
        else:
            regreso.append(new_trazado)
    return {"ida": ida, "regreso": regreso}


def get_vehicles(db: Session, region: int, comuna: str, calle: str) -> List[Dict]:
    raw_query = """
    SELECT S.nombre_responsable as nombre_responsable, V.patente AS patente, V.marca AS marca, V.modelo AS modelo, V.anho_fabricacion AS año_fabricacion FROM vehiculo V, servicio S
    WHERE S.region = :region
    AND V.s_region = :region AND V.s_folio IN (
        SELECT P.s_folio FROM pasapor P
        WHERE P.s_region = :region AND P.t_calle LIKE :calle AND P.t_comuna LIKE :comuna)
    AND S.folio = V.s_folio;
    """
    params = {"region": region, "comuna": comuna, "calle": calle}
    return exec_raw_query(db, raw_query, params)
