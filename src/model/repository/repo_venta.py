"""Consutlas de transacciones y ventas."""
from src.model.dto.venta import Venta
from src.model.dto.transaccion import Transaccion


def get_all_ventas():
    """Obtiene el usuario por correo."""
    return Venta.query.all()


def get_venta_by_ref(ref):
    """Obtiene la venta por referencia."""
    return Venta.query.get(ref)


def get_all_transacciones():
    """Obtiene usuarios con status = 1."""
    return Transaccion.query.all()


def get_transaccion_by_id(id_transaccion):
    """Obtiene la transaccion especifican."""
    return Transaccion.query.get(id_transaccion)


def get_transaccion_by_ref(id_referencia):
    """Obtiene la transaccion especifican."""
    return Transaccion.query.filter(Transaccion.id_referencia == id_referencia)


def get_all_transacciones_and_status():
    """Obtiene usuarios con status = 1."""
    return get_all_transacciones().filter(Transaccion.status == 1)
