"""Consultas con la tabla de categoría."""
from src.model.dto.tipo_producto import TipoProducto 


def get_all_tipo_productos():
    """Regresa todas las filas de producto."""
    return TipoProducto.query.all()


def get_tipo_by_id(id_producto):
    """Regresa el producto por id."""
    return TipoProoducto.query.get(id_producto)


def get_tipo_by_nombre(nombre):
    """Regresa el producto con el nombre especificado."""
    return TipoProducto.query.filter(TipoProducto.nombre == nombre).first()
