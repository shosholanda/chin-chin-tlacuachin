"""Consultas con la tabla de categoría."""
from src.model.dto.categoria import Categoria


def get_all_categorias():
    """Regresa todas las filas de producto."""
    return Categoria.query.all()


def get_categoria_by_id(id_producto):
    """Regresa el producto por id."""
    return Categoria.query.get(id_producto)


def get_categoria_by_nombre(nombre):
    """Regresa el producto con el nombre especificado."""
    return Categoria.query.filter(Categoria.nombre == nombre).first()
