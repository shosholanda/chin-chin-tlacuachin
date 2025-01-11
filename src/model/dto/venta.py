"""Tabla de ventas."""
import datetime
from src import db


class Venta(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: Venta
    La venta refencia a un grupo de transacciones donde además guarda
    con qué usuario y a qué sucursal.
    """

    __tablename__ = 'venta'
    referencia = db.Column('referencia', db.Integer, primary_key=True)
    id_usuario = db.Column(db.String(100), db.ForeignKey('usuario.correo'))
    # id_sucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'))
    cliente = db.Column('cliente', db.String(100))
    notas = db.Column('notas', db.String(200))
    # Total de la transacción sin propinas
    total = db.Column('total', db.Float(2), nullable=False)
    propina = db.Column('propina', db.Float(2), nullable=False)
    # Fecha y hora de la transacción
    fecha = db.Column('fecha', db.DateTime)

    transacciones = db.relationship('Transaccion', back_populates='venta')
    usuario = db.relationship('Usuario', back_populates='ventas')
    # sucursal = db.relationship('Sucursal', back_populates='ventas')

    # Constructor
    def __init__(self,
                 id_usuario,
                 total,
                 cliente="",
                 notas="",
                 propina=0):
        """Construye un objeto."""
        self.total = total
        self.id_usuario = id_usuario
        # self.id_sucursal = id_sucursal
        self.cliente = cliente
        self.notas = notas
        self.propina = propina
        self.fecha = datetime.datetime.now()

    # Representación en cadena
    def __repr__(self) -> str:
        """Representacion en cadena de este objeto."""
        return f'{self.referencia} : ${self.total} - {self.fecha}'
