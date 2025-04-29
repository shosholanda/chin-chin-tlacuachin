"""Controlador para consultar ventas.

Los reportes serán por corte (día, semana, mes, año) o particular.
También habrá reportes sobre el manejo de productos, insumos, filtros de búsqueda, graficas etc.
"""
from flask import (
    render_template, Blueprint, flash, redirect, render_template_string, request, url_for, session, abort
)

from src.model.dto.venta import Venta
from src.model.dto.transaccion import Transaccion
from src.model.dto.tipo_pago import TipoPago

from src.model.repository.repo import *
from src.model.repository.repo_producto import get_subgtin_and_status, get_producto_by_gtin
from src.model.repository.repo_venta import get_transaccion_by_ref

from src.controller.auth import requiere_inicio_sesion

reportes = Blueprint('reportes', __name__, url_prefix='/reporte/')


@reportes.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de reporte."""
    return render_template('cafeteria/reportes/resumen.html')
