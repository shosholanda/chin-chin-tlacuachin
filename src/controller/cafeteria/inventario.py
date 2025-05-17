"""Controlador para la página de INVENTARIO.

El inventario se registran como
ID | TIPO_ARTICULO | CANTIDAD |
Sin embargo, se guarda como articulo.
"""
from flask import (
    render_template, Blueprint, flash, redirect, render_template_string, request, url_for
)
from markupsafe import Markup

from src.model.entity.articulo import Articulo
from src.model.entity.tipo_articulo import TipoArticulo

from src.model.repository.repo import *


from src.controller.auth import requiere_inicio_sesion

inventario = Blueprint('inventario', __name__, url_prefix='/inventario')


@inventario.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de inventario."""
    page = request.args.get('page', default=1, type=int)
    paginacion= 20
    start = (page-1) * paginacion
    end = start + paginacion
    total = count_rows(Articulo)//paginacion 
    articulos = get_all(Articulo, limit=paginacion, offset=start, column='nombre', status=True)

    tipo_articulos = get_all(TipoArticulo)
    return render_template('cafeteria/inventario/inventario.html',
                           articulos=articulos,
                           tipo_articulos=tipo_articulos,
                           page=page, total=total)


@inventario.route('/<id_articulo>', methods=['GET', 'POST'])
@requiere_inicio_sesion
def articulo(id_articulo):
    """Página para visualizar solo un articulo."""
    articulo = get_by_id(Articulo, id_articulo)
    if not articulo:
        return redirect(url_for('inventario.main'))
    tipo_articulos = get_all(TipoArticulo)
    return render_template('cafeteria/inventario/articulo.html',
                           articulo=articulo,
                           tipo_articulos=tipo_articulos)


@inventario.route('get-articulo/<nombre_articulo>', methods=['GET'])
@requiere_inicio_sesion
def get_articulo(nombre_articulo):
    """Obtiene el articulo por nombre"""
    art = get_by_name(Articulo, nombre_articulo)
    if not art:
        return {'err': 'No se encontró el articulo'}
    return {'id': art.id,
            'nombre': art.nombre,
            'cantidad_actual': art.cantidad_actual,
            'status': art.status}

@inventario.route('get-articulos/<nombres_articulos>', methods=['GET'])
@requiere_inicio_sesion
def get_articulos(nombres_articulos):
    """Obtiene el articulos que coincidan por nombre"""
    arts = get_by_name(Articulo, nombres_articulos, all=True)
    return [{'id': art.id,
            'nombre': art.nombre,
            'unidad': art.unidad,
            'costo_unitario': art.costo_unitario,
            'status': art.status} for art in arts if art.status == 1]

@inventario.route('administrar/')
@requiere_inicio_sesion
def administracion():
    columns = ['ID', 
               'Nombre', 
               'Tipo de producto', 
               'Cantidad actual', 
               'Unidad', 
               'Mínimo', 
               'Máximo', 
               'Costo Unitario', 
               'status']

    page = request.args.get('page', default=1, type=int)
    paginacion= 100
    start = (page-1) * paginacion
    end = start + paginacion
    total = count_rows(Articulo)//paginacion
    articulos = get_all(Articulo, limit=paginacion, offset=start, column='nombre')
    ## WATAFACK IS THIS BULLSHOT
    filas = [ {'row_options': ['id=' + str(x.id)],
               'data': [
                   x.id,
                   Markup(f'<a href="{ url_for('inventario.articulo', id_articulo=x.id) }"> {x.nombre} </a>'),
                   x.tipo_articulo.nombre,
                   render_template_string('{% from "macro.html" import format_number %}' +
                                          '{{ format_number(' + str(x.cantidad_actual) + ') }}'),
                   x.unidad,
                   render_template_string('{% from "macro.html" import format_number %}' +
                                          '{{ format_number(' + str(x.minimo) + ') }}'),
                   render_template_string('{% from "macro.html" import format_number %}' +
                                          '{{ format_number(' + str(x.maximo) + ') }}'),
                   render_template_string('{% from "macro.html" import format_number %}' +
                                          '{{ format_number(' + str(x.costo_unitario) + ') }}'),
                   '✅' if x.status else '-'
               ]}  for x in articulos]

    return render_template('cafeteria/table.html', columnas = columns, filas=filas, 
                           page=page, total=total)

@inventario.route('create-tipo-articulo/', methods=('GET', 'POST'))
@requiere_inicio_sesion
def create_tipo_articulo():
    """Registra un tipo articulo en la base de datos."""
    if request.method == 'POST':
        body = request.json
        tipo_art = body['tipo_articulo'].upper()

        if not get_by_name(TipoArticulo, tipo_art):
            new_tipo_art = TipoArticulo(tipo_art)
            agrega(new_tipo_art)
            flash("Nuevo tipo articulo agregado")
        else:
            flash("Ya existe un tipo articulo con el mismo nombre")

    return redirect(url_for('inventario.main'))


@inventario.route('/create-articulo', methods=('GET', 'POST'))
@requiere_inicio_sesion
def create_articulo():
    """Registra un articulo con todos los datos en la base de datos."""
    if request.method == 'POST':
        body = request.json
        nom = body['nombre'].strip()
        tip = body['tipo_articulo']
        can = body['cantidad_actual']
        cos = body['costo_por_unidad']
        uni = body['unidad']
        min = body['minimo']
        max = body['maximo']
        max = max if max != "" else None
        if not get_by_name(Articulo, nom):
            new_art = Articulo(nom, tip, can, uni, min, max, cos)
            agrega(new_art)
            flash("Articulo agregado correctamente")
        else:
            flash("El artículo ya existe en el inventario. Intenta otro nombre")
    return redirect(url_for('inventario.main'))


@inventario.route('/update-articulo/<id_articulo>', methods=('GET', 'POST'))
@requiere_inicio_sesion
def update_articulo(id_articulo):
    """Registra un articulo con todos los datos en la base de datos."""
    if request.method == 'POST':
        body = request.json
        art = get_by_id(Articulo, id_articulo)
        art.id_tipo_articulo = body['tipo_articulo']
        art.cantidad_actual = body['cantidad_actual']
        art.costo_unitario = body['costo']
        art.unidad = body['unidad']
        art.minimo = body['minimo']
        max = body['maximo']
        art.maximo = max if max != "" else None
        agrega(art)
        flash("Articulo actualizado correctamente")
    # return redirect(url_for('inventario.articulo',
    #                         id_articulo=id_articulo))
    return redirect(url_for('inventario.main'))


@inventario.route('/eliminar-articulo/<id_articulo>')
@requiere_inicio_sesion
def delete_articulo(id_articulo):
    """Elimina el articulo para siempre."""
    articulo = get_by_id(Articulo, id_articulo)
    if articulo.receta == []:
        elimina(articulo)
    else:
        soft_delete(articulo)
    flash("Articulo eliminado con éxito")
    return redirect(url_for('inventario.main'))


@inventario.route('/change-status/<id_articulo>')
@requiere_inicio_sesion
def cambiar_status(id_articulo):
    """Elimina al articulo. Soft Delete."""
    articulo = get_by_id(Articulo, id_articulo)
    articulo.status = not articulo.status
    agrega(articulo)
    flash("Articulo cambiado con éxito")
    return redirect(url_for('inventario.main'))

