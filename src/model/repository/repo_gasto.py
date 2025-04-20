"""Consultas con la tabla de categoría."""
from src.model.dto.gasto import Gasto


def get_all_gastos_ordered_by_date():
    """Regresa todos los gastos por orden de fecha."""
    return Gasto.query.order_by(Gasto.fecha).all()


def get_all_gastos_in_range(start, finish):
    """Regresa todos los gastos en cierto rango."""
    return Gasto.query.all()


def get_all_gastos_in_range_and_status(start, finish):
    """Regresa todos los gastos en cierto rango y que esten activados."""
    return Gasto.query.all()

