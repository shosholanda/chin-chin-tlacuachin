"""Consultas con la tabla de categoría."""
from src.model.dto.tipo_gasto import TipoGasto


def get_all_tipo_gasto():
    """Regresa todas las filas de producto."""
    return TipoGasto.query.all()


def get_tipo_gasto_by_id(id_tipo_gasto):
    """Regresa el producto por id."""
    return TipoGasto.query.get(id_tipo_gasto)


def get_tipo_gasto_by_nombre(nombre):
    """Regresa el producto con el nombre especificado."""
    return TipoGasto.query.filter(TipoGasto.nombre == nombre).first()
