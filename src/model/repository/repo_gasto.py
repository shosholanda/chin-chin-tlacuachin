"""Consultas con la tabla de categoría."""
from src.model.dto.gasto import Gasto
from src import db
from sqlalchemy import func


def get_all_gastos_ordered_by_date():
    """Regresa todos los gastos por orden de fecha."""
    return Gasto.query.order_by(Gasto.fecha).all()


def get_all_gastos_in_range(start, finish):
    """Regresa todos los gastos en cierto rango."""
    return Gasto.query.all()


def get_all_gastos_in_range_and_status(start, finish):
    """Regresa todos los gastos en cierto rango y que esten activados."""
    return Gasto.query.all()

def get_sum_gasto_by_day(day):
    """Regresa los gastos hechos en un solo día."""
    return db.session.query(func.round(func.sum(Gasto.cantidad)))\
        .filter(func.date(Gasto.fecha) == day)\
        .scalar() or 0

