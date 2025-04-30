"""Consutlas de transacciones y ventas."""
from src.model.dto.venta import Venta
from src.model.dto.transaccion import Transaccion
from src.model.dto.receta import Receta
from src.model.dto.articulo import Articulo
from src.model.dto.producto import Producto

from src import db
from src.model.repository.repo import *
from sqlalchemy.sql import func


def get_transaccion_by_ref(id_referencia):
    """Obtiene la transaccion especifican."""
    return Transaccion.query.filter(Transaccion.id_referencia == id_referencia)

def get_total_productos(products):
    """Obtiene la suma total de insumos usados en estos productos"""
    return products.with_entities(func.round(func.sum(Receta.cantidad * Articulo.costo_unitario), 2))\
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
