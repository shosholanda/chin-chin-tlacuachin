"""Tabla de inventarios."""
from src import db


class Receta(db.Model):
    """Clase que modela una entidad con sus respectivos atributos.

    Entidad: Receta.
    Las recetas son solamente los insumos que se utilizan para un producto.
    Una lista de insumos por producto.
    """

    # Nombre de la tabla
    __tablename__ = 'receta'
    id = db.Column('id', db.Integer, primary_key=True)
    # Id de los ingredientes de este pnroducto
    id_producto = db.Column(db.Integer,
                            db.ForeignKey('producto.id'),
                            nullable=False)
    id_insumo = db.Column(db.Integer,
                          db.ForeignKey('articulo.id'),
                          nullable=False)
    # Cantidad requerida del insumo para hacer este producto.
    # La unidad es la misma que la del insumo
    cantidad = db.Column('cantidad', db.Float(3), nullable=False, default=0)
    status = db.Column('status', db.Boolean, nullable=False, default=True)

    producto = db.relationship('Producto', back_populates='receta')
    insumo = db.relationship('Articulo', back_populates='receta')

    def __init__(self,
                 id_producto,
                 id_insumo,
                 cantidad):
        """Crea un objeto."""
        self.id_producto = id_producto
        self.id_insumo = id_insumo
        self.cantidad = cantidad

    def __repr__(self) -> str:
        """Representación en cadena de este objeto."""
        return f'{self.producto.nombre}\n{self.insumo.nombre}\t{self.cantidad}'
    
    def precio_total(self):
        return round(self.cantidad * self.insumo.costo_unitario, 2)
