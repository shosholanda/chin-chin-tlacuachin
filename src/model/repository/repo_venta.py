"""Consutlas de transacciones y ventas."""
from src.model.dto.venta import Venta
from src.model.dto.transaccion import Transaccion


def get_transaccion_by_ref(id_referencia):
    """Obtiene la transaccion especifican."""
    return Transaccion.query.filter(Transaccion.id_referencia == id_referencia)
