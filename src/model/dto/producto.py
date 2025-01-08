"""Tabla de productos."""
from src import db
# WTF tengo q importar esta madres
# from src.model.tipo_producto import TipoProducto


class Producto(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: Producto
    Relaciona productos (que son vendidos) con un precio.
    """

    # Nombre de la tabla
    __tablename__ = 'producto'
    # PK
    id = db.Column('id', db.Integer, primary_key=True)
    gtin = db.Column('gtin', db.String(50), nullable=False, unique=True)
    nombre = db.Column('nombre', db.String(200), nullable=False)
    # ID de la categoria
    id_categoria = db.Column(db.Integer,
                             db.ForeignKey('categoria.id'),
                             nullable=False)
    # id del tipo
    id_tipo_producto = db.Column(db.Integer,
                                 db.ForeignKey('tipo_producto.id'),
                                 nullable=False)
    # Precio del producto.
    precio = db.Column('precio', db.Float(2), nullable=False)
    # Nos dice si sigue estando activo o no el producto.
    status = db.Column('status', db.Boolean, nullable=False, default=1)

    categoria = db.relationship('Categoria', back_populates='producto')
    tipo_producto = db.relationship('TipoProducto', back_populates='producto')

    # Constructor
    def __init__(self,
                 gtin,
                 nombre,
                 id_categoria,
                 id_tipo_producto,
                 precio):
        """Crea un objeto."""
        self.gtin = gtin
        self.nombre = nombre
        self.id_categoria = id_categoria
        self.id_tipo_producto = id_tipo_producto
        self.precio = precio

    # Representación en cadena
    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f"{self.gtin}\t{self.descripcion}\t${self.precio}"
