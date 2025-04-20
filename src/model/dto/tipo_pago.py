"""Tabla Tipo de producto."""
from src import db


class TipoPago(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: TipoPago
    Los diferentes TiposPago disponibles.
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_pago'
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column('nombre', db.String(40), nullable=False, unique=True)
    # Nos dice si sigue estando activo o no el tipo.
    status = db.Column('status', db.Boolean, nullable=False, default=True)

    ventas = db.relationship('Venta', back_populates='tipo_pago')

    def __init__(self,
                 nombre):
        """Crea un objeto."""
        self.nombre = nombre

    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f'{self.nombre}'
