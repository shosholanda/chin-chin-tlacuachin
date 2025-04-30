"""Consultas con la tabla de producto."""
from src.model.dto.producto import Producto
from src.model.dto.receta import Receta


def get_producto_by_gtin(gtin):
    """Regresa el producto con el gtin especificado."""
    return Producto.query.filter(Producto.gtin == gtin).first()


def get_subgtin(gtin):
    """Regresa los productos que contengan el código gtin."""
    return Producto.query.filter(Producto.gtin.contains(gtin))


def get_subgtin_and_status(gtin):
    """Regresa los productos activos que contengan gtin."""
    return get_subgtin(gtin).filter(Producto.status == 1)

def get_receta_by_product(id_producto):
    return Receta.query.filter(Receta.id_producto == id_producto)

def get_receta_by_insumo(id_insumo):
    return Receta.query.filter(Receta.id_insumo == id_insumo)

def get_insumo_in_receta(id_producto, id_insumo):
    return Receta.query.filter(Receta.id_insumo == id_insumo and Receta.id_producto == id_producto).first()
