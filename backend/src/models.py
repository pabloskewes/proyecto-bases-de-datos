from sqlalchemy import Column, Integer, String, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Servicio(Base):
    __tablename__ = "servicio"

    folio = Column(Integer, primary_key=True)
    region = Column(Integer, primary_key=True)
    tipo_servicio = Column(String)
    flota = Column(Integer)
    nombre_responsable = Column(String)


class Lugar(Base):
    __tablename__ = "lugar"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    comuna = Column(String, nullable=False)
    domicilio = Column(String)


class Trazado(Base):
    __tablename__ = "trazado"

    sentido = Column(String, primary_key=True)
    calle = Column(String, primary_key=True)
    comuna = Column(String, primary_key=True)


class Vehiculo(Base):
    __tablename__ = "vehiculo"

    patente = Column(String, primary_key=True)
    s_folio = Column(Integer, nullable=False)
    s_region = Column(Integer, nullable=False)
    marca = Column(String)
    fecha_ingreso = Column(Date)
    capacidad = Column(Integer)
    año_fabricacion = Column(Integer)
    modelo = Column(String)
    tipo_servicio = Column(String)

    servicio = relationship("Servicio", foreign_keys=[s_folio, s_region])


class Recorrido(Base):
    __tablename__ = "recorrido"

    nombre_recorrido = Column(String, primary_key=True)
    id_origen = Column(Integer, nullable=False)
    id_destino = Column(Integer, nullable=False)
    s_folio = Column(Integer, nullable=False)
    s_region = Column(Integer, nullable=False)

    # servicio = relationship("Servicio", foreign_keys=[s_folio, s_region])
    servicio = relationship(
        "Servicio",
        primaryjoin="and_(Recorrido.s_folio == Servicio.folio, Recorrido.s_region == Servicio.region)",
    )


class PasaPor(Base):
    __tablename__ = "pasapor"

    r_nombre_recorrido = Column(String, nullable=False, primary_key=True)
    r_calle = Column(String, nullable=False, primary_key=True)
    t_comuna = Column(String, nullable=False, primary_key=True)
    t_sentido = Column(String, nullable=False, primary_key=True)
    orden = Column(Integer)
    s_folio = Column(Integer, nullable=False, primary_key=True)
    s_region = Column(Integer, nullable=False, primary_key=True)

    recorrido = relationship(
        "Recorrido",
        primaryjoin="and_(PasaPor.s_folio == Recorrido.s_folio, PasaPor.s_region == Recorrido.s_region, PasaPor.r_nombre_recorrido == Recorrido.nombre_recorrido)",
    )

    # __table_args__ = (
    #     ForeignKeyConstraint(
    #         ["s_folio", "s_region", "r_nombre_recorrido"],
    #         ["recorrido.s_folio", "recorrido.s_region", "recorrido.nombre_recorrido"],
    #     ),
    #     ForeignKeyConstraint(
    #         ["t_sentido", "r_calle", "t_comuna"],
    #         ["trazado.sentido", "trazado.calle", "trazado.comuna"],
    #     ),
    #     # {
    #     #     "primary_key": (
    #     #         s_folio,
    #     #         s_region,
    #     #         r_nombre_recorrido,
    #     #         r_calle,
    #     #         t_comuna,
    #     #         t_sentido,
    #     #     )
    #     # },
    # )


# # Additional foreign key constraints for Recorrido table
# Servicio.recorridos = relationship(
#     "Recorrido", foreign_keys=[Recorrido.s_folio, Recorrido.s_region]
# )


# # Additional foreign key constraints for PasaPor table
# Recorrido.trazados = relationship(
#     "Trazado", foreign_keys=[PasaPor.t_sentido, PasaPor.r_calle, PasaPor.t_comuna]
# )
