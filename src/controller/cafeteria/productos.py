"""Controlador para la página de productos.

Los productos se registran completamente con
CATEGORIA | PRODUCTO | TIPO_PRODUCTO | PRECIO
"""
import math
from flask import (
    render_template, Blueprint, flash, redirect, request, url_for, get_flashed_messages
)

# from werkzeug.exceptions import abort

from src.model.dto.producto import Producto
from src.model.dto.categoria import Categoria
from src.model.dto.tipo_producto import TipoProducto
from src.model.dto.articulo import Articulo
from src.model.dto.receta import Receta

from src.model.repository.repo import *
from src.model.repository.repo_producto import *
from src.model.repository.repo_articulo import get_insumo_by_nombre

from src.controller.auth import requiere_inicio_sesion

productos = Blueprint('productos', __name__, url_prefix='/productos')


@productos.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de productos."""
    categorias = get_all_by_status(Categoria)
    tipos = get_all_by_status(TipoProducto)
    productos = get_all(Producto)[::-1]

    return render_template('cafeteria/productos/productos.html',
                           categorias=categorias,
                           tipo_productos=tipos,
                           productos=productos)


@productos.route('<gtin>/', methods=['GET', 'POST'])
@requiere_inicio_sesion
def producto(gtin):
    """Página para visualizar solo un producto."""
    producto = get_producto_by_gtin(gtin)
    if not producto: 
        return redirect(url_for('productos.main'))
    return render_template('cafeteria/productos/producto.html',
                           producto=producto)


@productos.route('get-insumo/<insumo>', methods=['GET'])
@requiere_inicio_sesion
def get_insumo(insumo):
    """Obtiene el insumo de la base de datos."""
    # Solo que la columna sea insumo
    pseudo_insumo = get_insumo_by_nombre(insumo)
    return {x.id: x.nombre for x in pseudo_insumo}


@productos.route('create-producto/', methods=['GET', 'POST'])
@requiere_inicio_sesion
def create_producto():
    """Registra un producto con todos los datos en la base de datos."""
    if request.method == 'POST':
        body = request.json
        if None in body.values() or len(body) != 5:
            flash("Rellena todos los campos", category="error")
            return redirect(url_for('productos.main'))
        gtin = body['gtin']
        if get_producto_by_gtin(gtin):
            flash("Ya existe el producto con este gtin", category="error")
            return redirect(url_for('productos.main'))
        nombre = body['nombre'].title()
        categoria = body['categoria']
        tipo_producto = body['tipo_producto']
        precio = body['precio']
        try:
            id_categoria = int(categoria)
            id_tipo_producto = int(tipo_producto)
            precio = float(precio)
        except ValueError:
            flash("Solo ingresa dígitos en precio tonoto.", category="error")
            return redirect(url_for('productos.main'))
        producto = Producto(gtin, nombre, id_categoria, id_tipo_producto, precio)
        agrega(producto)
        flash("Producto agregado correctamente", category="success")
    return redirect(url_for('productos.main'))


@productos.route('get-gtin/<gtin>', methods=['GET'])
@requiere_inicio_sesion
def get_gtin(gtin):
    """Obtiene el producto por gtin."""
    gtin_bdd = get_producto_by_gtin(gtin)
    code = None if not gtin_bdd else gtin_bdd.gtin
    response = {'gtin': code}
    return response


@productos.route('update-producto/', methods=['GET', 'POST'])
@requiere_inicio_sesion
def update_producto():
    """Actualiza el producto, a lo más el precio o status."""
    if request.method == 'POST':
        body = request.json
        # id_producto = body['id_producto']
        # nombre = body['nombre']
        gtin = body['gtin']
        precio = body['precio']

        used_gtin = get_producto_by_gtin(gtin)
        print(used_gtin.precio)
        print (precio)

        if used_gtin.precio != precio:
            #LMAO stupid decimal
            nuevo_gtin = used_gtin.gtin[:-len(str(math.trunc(precio)))] + str(math.trunc(precio))
            if used_gtin.transacciones == []:
                used_gtin.gtin = nuevo_gtin
                used_gtin.precio = precio
                flash("Producto actualizado a " + nuevo_gtin+ " sin duplicar")
                agrega(used_gtin)
            else:
                nuevo_producto = Producto(nuevo_gtin, 
                                        used_gtin.nombre,
                                        used_gtin.id_categoria,
                                        used_gtin.id_tipo_producto,
                                        precio)
                agrega(nuevo_producto)
                used_gtin.status = False
                agrega(used_gtin)
                print("Copia", nuevo_producto)
                flash("Precio de producto cambiado a " + nuevo_gtin)
        else:
            flash("Ningun cambio realizado", category='info')
            return redirect(url_for('productos.producto', gtin=gtin))
    return redirect(url_for('productos.main'))


@productos.route('delete-producto/<gtin>')
@requiere_inicio_sesion
def delete_producto(gtin):
    """Elimina el producto para siempre.

    No se puede eliminar si ya hay compras asociadas a este producto.
    """
    producto = get_producto_by_gtin(gtin)
    if producto and producto.transacciones == []:
        elimina(producto)
        flash("El producto se eliminó exitosamente", category="success")
    else:
        flash('''No se puede borrar el producto porque YA EXISTE UNA venta hecha con este producto.
              Puedes "ocultarlo" desactivando el status.''', category="error")
    return redirect(url_for('productos.main'))


@productos.route('change-status/<gtin>')
@requiere_inicio_sesion
def change_status(gtin):
    """Elimina al producto. Soft Delete."""
    producto = get_producto_by_gtin(gtin)
    producto.status = not producto.status
    agrega(producto)
    flash("Producto cambiado con éxito")
    return redirect(url_for('productos.main'))


@productos.route('create-tipo-producto/', methods=['POST', 'GET'])
@requiere_inicio_sesion
def create_tipo_producto():
    """Crea un nuevo tipo de producto si no existe."""
    if request.method == 'POST':
        body = request.get_json()
        nombre_tipo_producto = body['nombre'].upper()

        if not get_by_name(TipoProducto, nombre_tipo_producto):
            nuevo_tipo = TipoProducto(nombre_tipo_producto)
            agrega(nuevo_tipo)
            flash("Tipo creado correctamente:" + nombre_tipo_producto, category="success")
        else:
            flash("Ya existe un tipo con este nombre: " + nombre_tipo_producto, category="error")
    return redirect(url_for('productos.main'))


@productos.route('create-categoria/', methods=['POST', 'GET'])
@requiere_inicio_sesion
def create_categoria():
    """Crea una nueva categoria si no existe."""
    if request.method == 'POST':
        body = request.get_json()#['body']
        nombre_categoria = body['nombre'].title()
        if not get_by_name(Categoria, nombre_categoria):
            nueva_categoria = Categoria(nombre_categoria)
            agrega(nueva_categoria)
            flash("Categoria creada: " + nueva_categoria.nombre, category="success")
        else:
            flash("Ya existe una categoria con este nombre", category="error")
    return redirect(url_for('productos.main'))


@productos.route('delete-insumo/', methods=['GET', 'POST'])
@requiere_inicio_sesion
def delete_insumo():
    if request.method == 'POST':
        body = request.json
        producto = get_by_id(Producto, body['id_producto'])
        
        if not producto:
            flash("No se encontró el producto para eliminar el insumo")
            return redirect(url_for('productos.main' ))
        insumo = get_by_id(Articulo, body['id_insumo'])
        if not insumo:
            flash("No se encontró el insumo para eliminar")
            return redirect(url_for('productos.main' ))
        
        receta = get_insumo_in_receta(producto.id, insumo.id)
        if not receta: 
            flash("No se puede eliminar este insumo de este producto porque no están asociados")
            return redirect(url_for('productos.main' ))
        
        elimina(receta)
        
    flash("Insumo eliminado con éxito")
    return redirect(url_for('productos.producto', gtin=producto.gtin))

@productos.route('add-insumo/<gtin>', methods=['GET', 'POST'])
@requiere_inicio_sesion
def add_insumo(gtin):
    producto = get_producto_by_gtin(gtin)
    if not producto:
        flash("No se encontró el producto para agregar el insumo")
        return redirect(url_for('productos.main' ))
    if request.method == 'POST':
        print(request.form)
        id_articulo = request.form.get('id_articulo')
        cant = request.form.get('quantity')
        insumo = get_by_id(Articulo, id_articulo)
        if not insumo:
            flash("No se encontró el insumo " + str(id_articulo))
            return redirect(url_for('productos.producto', gtin=gtin))
        receta = Receta(producto.id, id_articulo, cant)
        agrega(receta)
    flash("Insumo agregado con éxito")
    return redirect(url_for('productos.producto', gtin=gtin))