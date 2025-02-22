"""Tabla de transacciones."""
from src import db


class Transaccion(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: Transaccion
    Imita la cantidad de productos que lleva un cliente.
    Todos los productos en la misma sesión deben tener el mismo identificador.
    """

    # Nombre de la tabla
    __tablename__ = 'transaccion'
    # PK
    id = db.Column('id', db.Integer, primary_key=True)
    id_referencia = db.Column(db.Integer, db.ForeignKey('venta.referencia'))
    # ID del producto
    id_producto = db.Column(db.Integer,
                            db.ForeignKey('producto.id'),
                            nullable=False)
    cantidad = db.Column('cantidad', db.Integer, default=0)
    # Para cancelar ventas
    status = db.Column('status', db.Boolean, nullable=False, default=1)

    venta = db.relationship('Venta', back_populates='transacciones')
    producto = db.relationship('Producto', back_populates='transacciones')

    # Constructor
    def __init__(self,
                 id_referencia,
                 id_producto,
                 cantidad):
        """Crea un objeto."""
        self.id_referencia = id_referencia
        self.id_producto = id_producto
        self.cantidad = cantidad

    # Representación en cadena
    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f'{self.id_referencia}\t{self.producto.nombre}\t{self.cantidad}'
