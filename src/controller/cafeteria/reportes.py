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
from src.model.repository.repo_gasto import *
from src.model.repository.repo_venta import *

from src.controller.auth import requiere_inicio_sesion

reportes = Blueprint('reportes', __name__, url_prefix='/reporte/')


@reportes.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de reporte."""
    return render_template('cafeteria/reportes/resumen.html')


@reportes.route('utilidad/')
@requiere_inicio_sesion
def utilidad():
    ini = request.args.get('start-date')
    fin = request.args.get('end-date')

    ini = dt.datetime.strptime(ini,'%Y-%m-%d').date() if ini else (dt.date.today() - dt.timedelta(days=30))
    fin = dt.datetime.strptime(fin, '%Y-%m-%d').date() if fin else dt.date.today()

    days = []
    ganancia_bruta = []
    costos_productos = []
    utilidad_bruta = []
    costos_fijos = []
    utilidad_neta = []
    promedio = []
    avg = 0
    cont = 1
    
    while ini <= fin:
        days.append(ini)
        # Dado que puede haber días que no se laboren, no se puede confiar en la query
        # days = [01, 02, 03], ventas = [01, 03, 04] a menos que se haga un left join 
        # pero cómo si no existe ese día en las ventas? se debe crear el rango en mysql
        total_per_day = get_sum_productos_vendidos_by_day(ini)
        invest_per_day = get_sum_insumos_de_productos_vendidos_by_day(ini)
        raw_utility = total_per_day - invest_per_day
        fixed_costs = get_sum_gasto_by_day(ini)
        total_utility = raw_utility - fixed_costs
        ganancia_bruta.append(total_per_day)
        costos_productos.append(invest_per_day)
        utilidad_bruta.append(raw_utility)
        costos_fijos.append(fixed_costs)
        utilidad_neta.append(total_utility)
        avg += total_utility/cont
        cont += 1
        promedio.append(avg)

        ini = ini + dt.timedelta(days=1)

    data = {
        'ganancia_bruta': sum(ganancia_bruta),
        'costos_productos': sum(costos_productos),
        'utilidad_bruta': sum(utilidad_bruta),
        'costos_fijos': sum(costos_fijos),
        'utilidad_neta': sum(utilidad_neta)
    }

    container = render_template('cafeteria/reportes/container.html', data=data)

    return {
        'x_data': [d.strftime('%d %b %Y') for d in days],
        'y_data': {
            'ganancia_bruta': ganancia_bruta,
            'costos_productos': costos_productos,
            'utilidad_bruta': utilidad_bruta,
            'costos_fijos': costos_fijos,
            'utilidad_neta': utilidad_neta,
            'promedio': promedio
        },
        'container': container
    }


@reportes.route('corte/')
@requiere_inicio_sesion
def cortes():
    return render_template('cafeteria/reportes/cortes.html')