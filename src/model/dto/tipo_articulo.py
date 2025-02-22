"""Tabla Tipo de producto."""
from src import db


class TipoArticulo(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: Tipo
    Los diferentes Tipos para los diferentes articulos.
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_articulo'
    id = db.Column('id', db.Integer, primary_key=True)
    # Tipo del tipo completo
    nombre = db.Column('nombre', db.String(40), nullable=False, unique=True)
    # Nos dice si sigue estando activo o no el tipo.
    status = db.Column('status', db.Boolean, nullable=False, default=True)

    articulos = db.relationship('Articulo', back_populates='tipo_articulo')

    def __init__(self,
                 nombre):
        """Crea un objeto."""
        self.nombre = nombre

    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f'{self.nombre}'
