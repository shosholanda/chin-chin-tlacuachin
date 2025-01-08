"""Consultas con la tabla de producto."""
from src.model.dto.producto import Producto


def get_all_productos():
    """Regresa todas las filas de producto."""
    return Producto.query.all()


def get_producto_by_id(id_producto):
    """Regresa el producto por id."""
    return Producto.query.get(id_producto)


def get_producto_by_nombre(nombre):
    """Regresa el/los producto/s con el nombre especificado."""
    return Producto.query.filter(Producto.nombre == nombre).all()


def get_producto_by_gtin(gtin):
    """Regresa el producto con el gtin especificado."""
    return Producto.query.filter(Producto.gtin == gtin).first()
