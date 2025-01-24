"""Tabla de inventarios."""
from src import db


class Articulo(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: Articulo

    La información necesaria de un artículo del inventario.
    """

    # Nombre de la tabla
    __tablename__ = 'articulo'
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column('nombre', db.String(100), nullable=False, unique=True)
    # Cantidad que esta actualmente en el articulo. 3.450
    cantidad_actual = db.Column('cantidad_actual', db.Float(3), nullable=False, default=0)
    # Cómo se mide este producto. kg, gr, lt, ml, oz, pg, etc
    unidad = db.Column('unidad', db.String(2), nullable=False, default="un")
    # Cantidades a almacenar
    minimo = db.Column('minimo', db.Float(3), default=0)
    maximo = db.Column('maximo', db.Float(3))
    # Precio de 1 "algo" de esto.
    costo_unitario = db.Column('costo_unitario', db.Float(2), nullable=False, default=0)
    status = db.Column('status', db.Boolean, nullable=False, default=True)

    def __init__(self,
                 nombre,
                 cantidad_actual,
                 unidad,
                 minimo,
                 maximo,
                 costo_unitario):
        """Crea un objeto."""
        self.nombre = nombre
        self.cantidad_actual = cantidad_actual
        self.unidad = unidad
        self.minimo = minimo
        self.maximo = maximo
        self.costo_unitario = costo_unitario

    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f'{self.nombre}\t{self.cantidad_actual}\t{self.unidad}\t{self.costo_unitario}'
