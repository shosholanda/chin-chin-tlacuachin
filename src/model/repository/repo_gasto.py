"""Consultas con la tabla de categoría."""
from src.model.dto.gasto import Gasto


def get_all_gastos():
    """Regresa todas las filas de producto."""
    return Gasto.query.all()


def get_all_gastos_ordered_by_date():
    """Regresa todos los gastos por orden de fecha."""
    return Gasto.query.order_by(Gasto.fecha).all()


def get_all_gastos_by_date(date):
    """Regresa todos los gastos en cierta fecha."""
    return Gasto.query.all()


def get_all_gastos_and_status():
    """Regresa todos los gastos cuyo status sean 1."""
    return Gasto.query.filter(Gasto.status == 1)


def get_all_gastos_in_range(start, finish):
    """Regresa todos los gastos en cierto rango."""
    return Gasto.query.all()


def get_all_gastos_in_range_and_status(start, finish):
    """Regresa todos los gastos en cierto rango y que esten activados."""
    return Gasto.query.all()


def get_gasto_by_id(id_gasto):
    """Regresa el producto por id."""
    return Gasto.query.get(id_gasto)


def get_gastos_by_nombre(nombre):
    """Regresa el producto con el nombre especificado."""
    return Gasto.query.filter(Gasto.nombre == nombre).first()
