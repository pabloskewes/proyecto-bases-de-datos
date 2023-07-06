import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("HOST")
db_port = os.getenv("PUERTO")
db_name = os.getenv("DB")
db_user = os.getenv("USUARIO")
db_password = os.getenv("PASSWORD")

if db_host is None:
    raise ValueError("No se ha definido la variable de entorno HOST")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def create_user():
#     with engine.connect() as conection:
#         conection.execute("CREATE USER pudinPoof WITH PASSWORD 'poof'")
#         conection.execute("GRANT CONNECT ON DATABASE SQLALCHEMY_DATABASE_URL TO pudinPoof")
#         conection.execute("GRANT USAGE ON SCHEMA pudin TO pudinPoof")
#         conection.execute("GRANT SELECT ON ALL TABLES IN SCHEMA pudin TO pudinPoof")
#         conection.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA pudin GRANT SELECT ON TABLES TO pudinPoof")
        
# create_user()
