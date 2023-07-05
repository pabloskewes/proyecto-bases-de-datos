import os
import sqlalchemy
import pandas as pd
from tabulate import tabulate
import dotenv

dotenv.load_dotenv()


def print_table(df: pd.DataFrame) -> None:
    """Prints a DataFrame as a table using tabulate"""
    print(tabulate(df, headers="keys", tablefmt="psql"))


class SQLConnection:
    def __init__(self, engine: sqlalchemy.engine.base.Engine):
        self.engine = engine
        self.inspector = sqlalchemy.inspect(engine)

    @classmethod
    def from_url(cls, url: str):
        print(f"Connecting to {url}")
        engine = sqlalchemy.create_engine(url)
        return cls(engine)

    @classmethod
    def from_db(
        cls,
        sistema: str,
        usuario: str,
        contraseña: str,
        host: str,
        puerto: int,
        db: str,
    ):
        url = f"{sistema}://{usuario}:{contraseña}@{host}:{puerto}/{db}"
        return cls.from_url(url)

    @classmethod
    def from_env(cls):
        sistema = os.getenv("SISTEMA")
        usuario = os.getenv("USUARIO")
        contraseña = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        puerto = os.getenv("PUERTO")
        db = os.getenv("DB")
        return cls.from_db(sistema, usuario, contraseña, host, puerto, db)

    def query(self, query: str) -> pd.DataFrame:
        """Ejecuta una query y retorna el resultado como un DataFrame"""
        return pd.read_sql(query, self.engine)

    def analyse(self, query: str) -> pd.DataFrame:
        """Ejecuta una query con EXPLAIN ANALYZE y retorna el resultado como un DataFrame"""
        return self.query(f"EXPLAIN ANALYZE {query}")

    def execute(self, query: str) -> str:
        """Ejecuta una query usando el método execute de sqlalchemy"""
        with self.engine.connect() as connection:
            connection.execute(sqlalchemy.text(query))
        # return query output
        # return connection.connection.notices[-1]
