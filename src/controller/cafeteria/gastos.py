"""Controlador para la página de gastos.

Los gastos se registran como
ID | TIPO_GASTO | CANTIDAD |
"""
from flask import (
    render_template, Blueprint, flash, redirect, request, url_for
)

from src.model.dto.tipo_gasto import TipoGasto
from src.model.dto.gasto import Gasto

from src.model.repository.repo import *
from src.model.repository.repo_gasto import get_all_gastos_ordered_by_date

from src.controller.auth import requiere_inicio_sesion

gastos = Blueprint('gastos', __name__, url_prefix='/gastos')


@gastos.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de gastos."""
    gastos = get_all_gastos_ordered_by_date()[::-1]
    tipo_gastos = get_all(TipoGasto)
    return render_template('cafeteria/gastos/gastos.html',
                           gastos=gastos,
                           tipo_gastos=tipo_gastos)


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
        print(body)

        gasto.id_tipo_gasto = tipo_gasto
        gasto.cantidad = cantidad
        gasto.descripcion = descripcion
        gasto.fecha = fecha
        gasto.status = status
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
