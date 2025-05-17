"""Tabla Tipo de gasto."""
from src import db


class TipoGasto(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: TipoGasto
    Los diferentes Tipos de gastos para no repetir.
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_gasto'
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column('nombre', db.String(40), nullable=False, unique=True)
    descripcion = db.Column('descripcion', db.String(200))

    gasto = db.relationship('Gasto', back_populates='tipo_gasto')

    def __init__(self,
                 nombre,
                 descripcion="Sin descripción"):
        """Crea un objeto."""
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f'{self.nombre}'
