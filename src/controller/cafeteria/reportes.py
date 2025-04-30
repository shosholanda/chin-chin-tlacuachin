"""Controlador para consultar ventas.

Los reportes serán por corte (día, semana, mes, año) o particular.
También habrá reportes sobre el manejo de productos, insumos, filtros de búsqueda, graficas etc.
"""
from flask import (
    render_template, Blueprint, flash, redirect, render_template_string, request, url_for, session, abort
)

from src.model.dto.venta import Venta
from src.model.dto.gasto import Gasto
from src.model.dto.transaccion import Transaccion
from src.model.dto.tipo_pago import TipoPago

from src.model.repository.repo import *
from src.model.repository.repo_producto import get_subgtin_and_status, get_producto_by_gtin
from src.model.repository.repo_venta import *

from src.controller.auth import requiere_inicio_sesion

reportes = Blueprint('reportes', __name__, url_prefix='/reporte/')


@reportes.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de reporte."""
    ganancias = get_by_fecha(Venta)
    ganancia_bruta = sum_column(Venta, 'total', query=ganancias.subquery())
    costos_productos = get_total_productos(ganancias)
    costos = get_by_fecha(Gasto).subquery()
    costos_fijos = sum_column(Gasto, 'cantidad', query=costos)
    utilidad_bruta = ganancia_bruta - costos_productos
    utilidad_neta = utilidad_bruta - costos_fijos
    data = {
        'ganancia_bruta': ganancia_bruta,
        'costos_productos': costos_productos,
        'utilidad_bruta': utilidad_bruta,
        'costos_fijos': costos_fijos,
        'utilidad_neta': utilidad_neta,
        'data': {
            'xcord': [],
            'ycord': []
        }
    }
    return render_template('cafeteria/reportes/resumen.html', data=data)


@reportes.route('corte/')
@requiere_inicio_sesion
def cortes():
    return render_template('cafeteria/reportes/cortes.html')