"""Tabla de categoría."""
from src import db


class Categoria(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: Categoría
    Las categorías sirven para etiquetar productos por grupo.
    """

    # Nombre de la tabla
    __tablename__ = 'categoria'
    id = db.Column('id', db.Integer, primary_key=True)
    # Nombre de la categoría.
    nombre = db.Column('nombre', db.String(100), nullable=False, unique=True)
    # Descripción del producto (opcional)
    descripcion = db.Column('descripcion', db.String(200))

    # Pertenecer
    producto = db.relationship('Producto', back_populates='categoria')

    # Constructor
    def __init__(self,
                 nombre,
                 descripcion="Sin descripcion"):
        """Crea una nueva fila."""
        self.nombre = nombre
        self.descripcion = descripcion

    # Representación en cadena
    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f'{self.nombre}'
