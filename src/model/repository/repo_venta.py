"""Consutlas de transacciones y ventas."""
from src.model.entity.venta import Venta
from src.model.entity.transaccion import Transaccion
from src.model.entity.receta import Receta
from src.model.entity.articulo import Articulo
from src.model.entity.producto import Producto

from src import db
from src.model.repository.repo import *
from sqlalchemy.sql import func
import datetime as dt


def get_transaccion_by_ref(id_referencia):
    """Obtiene la transaccion especifican."""
    return Transaccion.query.filter(Transaccion.id_referencia == id_referencia)

def get_total_productos(products):
    """Obtiene la suma total de insumos usados en estos productos"""
    return products.with_entities(func.round(func.sum(Receta.cantidad * Articulo.costo_unitario * Transaccion.cantidad), 2))\
            .join(Venta.transacciones)\
            .join(Transaccion.producto)\
            .join(Producto.receta)\
            .join(Receta.insumo)\
            .scalar()
    

def get_sum_costo_producto(id_producto):
    """Obtiene la suma total de insumo usados en este producto."""
    return db.session.query(func.round(func.sum(Receta.cantidad * Articulo.costo_unitario), 2))\
            .filter(Producto, Producto.id == id_producto)\
            .filter(Receta, Receta.status == 1)\
            .join(Producto, Producto.id == Receta.id_producto)\
            .join(Articulo, Articulo.id == Receta.id_insumo).scalar()


def get_sum_productos_vendidos_by_day(day):
    return db.session.query(func.sum(Venta.total))\
            .filter(func.date(Venta.fecha) == day)\
            .order_by(func.date(Venta.fecha)).scalar() or 0


def get_sum_insumos_de_productos_vendidos_by_day(day):
     return db.session.query(func.round(func.sum(Receta.cantidad * Articulo.costo_unitario * Transaccion.cantidad), 2))\
            .filter(func.date(Venta.fecha) == day)\
            .join(Venta.transacciones)\
            .join(Transaccion.producto)\
            .join(Producto.receta)\
            .join(Receta.insumo)\
            .scalar() or 0


def get_sum_all_productos_vendidos_by_day():
    return db.session.query(func.date(Venta.fecha), func.coalesce(func.sum(Venta.total), 0))\
            .group_by(func.date(Venta.fecha))\
            .order_by(func.date(Venta.fecha)).all()
