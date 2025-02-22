"""Controlador para la página de productos.

Los productos se registran completamente con
CATEGORIA | PRODUCTO | TIPO_PRODUCTO | PRECIO
"""
from flask import (
    render_template, Blueprint, flash, redirect, request, url_for, get_flashed_messages
)

# from werkzeug.exceptions import abort

from src.model.dto.producto import Producto
from src.model.dto.categoria import Categoria
from src.model.dto.tipo_producto import TipoProducto
from src.model.dto.tipo_articulo import TipoArticulo
from src.model.dto.receta import Receta

from src.model.repository.repo import agrega, elimina
from src.model.repository.repo_producto import get_all_productos, get_producto_by_gtin, get_producto_by_id
from src.model.repository.repo_tipo_producto import get_tipo_by_nombre, get_all_tipo_productos
from src.model.repository.repo_categoria import get_all_categorias, get_categoria_by_nombre
from src.model.repository.repo_articulo import get_insumo_by_nombre
# from src.model.repository.repo_usuario import get

from src.controller.auth import requiere_inicio_sesion

productos = Blueprint('productos', __name__, url_prefix='/productos')


@productos.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de productos."""
    categorias = get_all_categorias()
    tipos = get_all_tipo_productos()
    productos = get_all_productos()[::-1]

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
        print(body)
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
    body = request.json
    id_producto = body['id_producto']
    nombre = body['nombre']
    gtin = body['gtin']
    producto = get_producto_by_id(id_producto)
    used_gtin = get_producto_by_gtin(gtin)

    # It may change 
    if used_gtin.gtin == producto.gtin or used_gtin == None:
        try:
            producto.nombre = nombre
            producto.gtin = gtin
            producto.precio = float(body['precio'])

            agrega(producto)
        except:
            flash("Ingresa valores válidos.")
    else:
        flash("No puedes usar este GTIN porque ya existe un producto con este código.\n" + used_gtin)
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

        if not get_tipo_by_nombre(nombre_tipo_producto):
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
        if not get_categoria_by_nombre(nombre_categoria):
            nueva_categoria = Categoria(nombre_categoria)
            agrega(nueva_categoria)
            flash("Categoria creada: " + nueva_categoria.nombre, category="success")
        else:
            flash("Ya existe una categoria con este nombre", category="error")
    return redirect(url_for('productos.main'))