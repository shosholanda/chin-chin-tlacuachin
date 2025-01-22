"""Tabla de gastos."""
from src import db
import datetime as dt


class Gasto(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: Gasto
    Un gasto es la resta a las ganacias para mantener activo el negocio.
    """

    # Nombre de la tabla
    __tablename__ = 'gasto'
    # PK
    id = db.Column('id', db.Integer, primary_key=True)
    descripcion = db.Column('descripcion', db.String(200), nullable=False, default="")
    id_tipo_gasto = db.Column(db.Integer,
                              db.ForeignKey('tipo_gasto.id'),
                              nullable=False)
    # Cantidad de este gasto.
    cantidad = db.Column('cantidad', db.Float(2), nullable=False, default=0)
    fecha = db.Column('fecha', db.DateTime)
    # Nos dice si sigue estando activo o no el producto.
    status = db.Column('status', db.Boolean, nullable=False, default=1)

    tipo_gasto = db.relationship('TipoGasto', back_populates='gasto')

    # Constructor
    def __init__(self,
                 descripcion,
                 id_tipo_gasto,
                 cantidad,
                 fecha=dt.datetime.now()):
        """Crea un objeto."""
        self.descripcion = descripcion
        self.id_tipo_gasto = id_tipo_gasto
        self.cantidad = cantidad
        self.fecha = fecha

    # Representación en cadena
    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f'{self.tipo_gasto.nombre}\t{self.cantidad}'
