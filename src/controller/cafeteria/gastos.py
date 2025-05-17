"""Controlador para la página de gastos.

Los gastos se registran como
ID | TIPO_GASTO | CANTIDAD |
"""
from flask import (
    render_template, Blueprint, flash, redirect, render_template_string, request, url_for
)
from markupsafe import Markup

from src.model.entity.tipo_gasto import TipoGasto
from src.model.entity.gasto import Gasto

from src.model.repository.repo import *

from src.controller.auth import requiere_inicio_sesion

gastos = Blueprint('gastos', __name__, url_prefix='/gastos')


@gastos.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de gastos."""

    page = request.args.get('page', default=1, type=int)
    paginacion= 20
    start = (page-1) * paginacion
    end = start + paginacion
    total = count_rows(Gasto, status=True)//paginacion 

    gastos = get_all(Gasto, limit=paginacion, offset=start, order='DESC', column='fecha', status=True)

    tipo_gastos = get_all(TipoGasto, status=True)
    return render_template('cafeteria/gastos/gastos.html',
                           gastos=gastos,
                           tipo_gastos=tipo_gastos, 
                           page=page, total=total)

@gastos.route('fecha/', methods=['GET'])
@requiere_inicio_sesion
def fecha():
    """Visualiza las últimas ventas realizadas en el periodo timespan"""
    fin = ini = filter = None
    start = request.args.get('start-date')
    end = request.args.get('end-date')
    filter = request.args.get('filter')
    period = request.args.get('period')

    ini = dt.datetime.strptime(start, "%Y-%m-%d")
    if period == 'day':
        fin = dt.datetime.strptime(start + ' 23:59:59', "%Y-%m-%d %H:%M:%S")
    elif period == 'week':
        fin = ini + dt.timedelta(days=8)
    elif period == 'month':
        fin = ini + dt.timedelta(days=30)
    else:
        fin = dt.datetime.strptime(end + ' 23:59:59', "%Y-%m-%d %H:%M:%S")
    gastos = get_by_fecha(Gasto, ini, fin).order_by(Gasto.id.desc())
    if filter != 'NaN':
        gastos = gastos.join(Gasto.tipo_gasto).filter(TipoGasto.id == filter)
    
    columns = ["ID", "Tipo Gasto", "Descripcion", "Cantidad", "Fecha"]
    filas = [ {'data': [
                    f'<a href="{ url_for('gastos.gasto', id_gasto=x.id) }"> {x.id} </a>',
                    x.tipo_gasto, 
                    x.descripcion,
                    render_template_string('{% from "macro.html" import format_number %}' +
                                           '${{ format_number(x) }}', x=x.cantidad),
                    render_template_string('{% from "macro.html" import format_date %}' + 
                                           '{{ format_date(fecha) }}', fecha = x.fecha),
                ]} for x in gastos ]
    total = sum_column(Gasto, 'cantidad', gastos)
    extra = [ {'data': [
                "",
                "",
                "Suma:", 
                render_template_string('{% from "macro.html" import format_number %}' +
                                           '${{ format_number(x) }}', x=total),
                ""
            ]}]
    table = render_template_string('' + 
            '{% from "macro.html" import table %}' +
            '{{ table(columns, filas, extra) }}', columns=columns, filas=filas, extra=extra)
    # WATAFACK SE VE Q HE MEJORADO ++
    return table



@gastos.route('periodo/', methods=['GET'])
@requiere_inicio_sesion
def periodo():
    """Regresa los gastos realizadas en el periodo timespan"""
    today = dt.date.today()
    timespan = request.args.get('period', 'day', str)
    ini = fin = today
    if timespan == 'day':
        pass
    elif timespan == 'week':
        ini = (dt.datetime.now() - dt.timedelta(days=7)).date()
    elif timespan == 'month':
        ini = (dt.datetime.now() - dt.timedelta(days=30)).date()

    tipo_gastos = get_all(TipoGasto) + [None]
    return render_template('cafeteria/gastos/periodo.html', timespan=timespan, filter=tipo_gastos,
                           ini=ini, fin=fin)




@gastos.route('/<id_gasto>', methods=['GET', 'POST'])
@requiere_inicio_sesion
def gasto(id_gasto):
    """Página para visualizar solo un gasto."""
    gasto = get_by_id(Gasto, id_gasto)
    tipo_gastos = get_all(TipoGasto)
    if not gasto:
        return redirect(url_for('gastos.main'))
    return render_template('cafeteria/gastos/gasto.html', gasto=gasto, tipo_gastos=tipo_gastos)


@gastos.route('/create-gasto', methods=('GET', 'POST'))
@requiere_inicio_sesion
def create_gasto():
    """Registra un gasto con todos los datos en la base de datos."""
    if request.method == 'POST':
        body = request.json
        desc = body['descripcion']
        tipo = int(body['tipo_de_gasto'])
        cant = float(body['cantidad'])
        fech = body['fecha']

        nuevo_gasto = Gasto(desc, tipo, cant, fech)
        agrega(nuevo_gasto)

        flash("Gasto agregado correctamente")
    return redirect(url_for('gastos.main'))


@gastos.route('/eliminar-gasto/<id_gasto>')
@requiere_inicio_sesion
def delete_gasto(id_gasto):
    """Elimina el gasto para siempre."""
    gasto = get_by_id(Gasto, id_gasto)
    elimina(gasto)
    flash("Gasto eliminado con éxito")
    return redirect(url_for('gastos.main'))

@gastos.route('/actualizar-gasto/<id_gasto>', methods=['GET', 'POST'])
@requiere_inicio_sesion
def update_gasto(id_gasto):
    """Modifica el gasto para siempre."""
    if request.method == 'POST':
        gasto = get_by_id(Gasto, id_gasto)
        body = request.json
        tipo_gasto = body['tipo_gasto']
        cantidad = body['cantidad']
        descripcion = body['descripcion']
        fecha = body['fecha']
        status = body['status']

        gasto.id_tipo_gasto = tipo_gasto
        gasto.cantidad = cantidad
        gasto.descripcion = descripcion
        gasto.fecha = fecha
        gasto.status = True if status == 'on' else False
        agrega(gasto)

        flash("Gasto modificado con éxito")
    return redirect(url_for('gastos.main'))



@gastos.route('/change-status/<id_gasto>')
@requiere_inicio_sesion
def change_status(id_gasto):
    """Elimina al gasto. Soft Delete."""
    gasto = get_by_id(Gasto, id_gasto)
    gasto.status = not gasto.status
    agrega(gasto)
    flash("Gasto cambiado con éxito")
    return redirect(url_for('gastos.main'))


@gastos.route('/crear-tipo-gasto', methods=['POST', 'GET'])
@requiere_inicio_sesion
def create_tipo_gasto():
    """Crea un nuevo tipo de gasto si no existe."""
    if request.method == 'POST':
        body = request.json
        tipo_gasto_nuevo = body['nombre']
        if not get_by_name(TipoGasto, tipo_gasto_nuevo):
            nuevo_tipo = TipoGasto(tipo_gasto_nuevo)
            agrega(nuevo_tipo)
            flash("Tipo creado correctamente")
        else:
            flash("Ya existe un tipo con este nombre")

    return redirect(url_for("gastos.main"))




@gastos.route('administracion/')
@requiere_inicio_sesion
def administracion():
    page = request.args.get('page', default=1, type=int)
    paginacion= 100
    start = (page-1) * paginacion
    end = start + paginacion
    total = count_rows(Gasto)//paginacion 

    columnas = ['ID', 'Tipo de gasto', 'Descripcion', 'Cantidad', 'Fecha', 'Status']

    gastos = get_all(Gasto, limit=paginacion, offset=start, order='DESC', column='fecha')
    filas = [ {'data': [
                    Markup(f'<a href="{ url_for('gastos.gasto', id_gasto=x.id) }"> {x.id} </a>'),
                    x.tipo_gasto,
                    x.descripcion,
                    render_template_string('{% from "macro.html" import format_number %}' +
                                          '$ {{ format_number(n) }}', n = x.cantidad),
                    Markup(render_template_string('{% from "macro.html" import format_date %}' + 
                                           '{{ format_date(fecha) }}', fecha = x.fecha)),
                   '✅' if x.status else '-'
               ]}  for x in gastos]

    return render_template('cafeteria/table.html',
                           columnas=columnas,
                           filas=filas,
                           page=page, total=total, 
                           siguiente= url_for('gastos.administracion', page=page+1),
                           anterior = url_for('gastos.administracion', page=page-1))