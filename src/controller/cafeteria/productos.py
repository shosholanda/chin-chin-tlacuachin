"""Controlador para la página de productos.

Los productos se registran completamente con
CATEGORIA | PRODUCTO | TIPO_PRODUCTO | PRECIO
"""
from flask import (
    render_template, Blueprint, flash, redirect, request, url_for
)

# from werkzeug.exceptions import abort

from src.model.dto.producto import Producto
from src.model.dto.categoria import Categoria
from src.model.dto.tipo_producto import TipoProducto

from src.model.repository.repo import agrega, elimina
from src.model.repository.repo_producto import get_all_productos, get_producto_by_gtin
from src.model.repository.repo_tipo_producto import get_tipo_by_nombre, get_all_tipo_productos
from src.model.repository.repo_categoria import get_all_categorias, get_categoria_by_nombre
# from src.model.repository.repo_usuario import get

from src.controller.auth import requiere_inicio_sesion

productos = Blueprint('productos', __name__, url_prefix='/productos')


@productos.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de productos."""
    categorias = get_all_categorias()
    tipos = get_all_tipo_productos()
    productos = get_all_productos()

    return render_template('cafeteria/productos/productos.html',
                           categorias=categorias,
                           tipo_productos=tipos,
                           productos=productos)


@productos.route('/<gtin>', methods=['GET', 'POST'])
@requiere_inicio_sesion
def producto(gtin):
    """Página para visualizar solo un producto."""
    pass


@productos.route('/create-producto', methods=('GET', 'POST'))
@requiere_inicio_sesion
def create_producto():
    """Registra un producto con todos los datos en la base de datos."""
    if request.method == 'POST':
        body = request.json
        if None in body.values() or len(body) != 5:
            flash("Rellenar todos los campos")
            return redirect(url_for('productos.main'))
        gtin = body['gtin']
        if get_producto_by_gtin(gtin):
            flash("Ya existe el producto")
            return redirect(url_for('productos.main'))
        nombre = body['nombre']
        categoria = body['categoria']
        tipo_producto = body['tipo_producto']
        precio = body['precio']
        try:
            precio = float(precio)
        except ValueError:
            flash("Solo ingresa dígitos en precio tonoto.")
        producto = Producto(gtin, nombre, categoria, tipo_producto, precio)
        agrega(producto)
        flash("Producto agregado correctamente")
    return redirect(url_for('productos.main'))


@productos.route('/get-gtin/<gtin>', methods=['GET'])
@requiere_inicio_sesion
def get_gtin(gtin):
    """Obtiene el producto por gtin."""
    gtin_bdd = get_producto_by_gtin(gtin)
    code = None if not gtin_bdd else gtin_bdd.gtin
    response = {'gtin': code}
    return response


@productos.route('/eliminar-producto/<gtin>')
@requiere_inicio_sesion
def delete_producto(gtin):
    """Elimina el producto para siempre.

    No se puede eliminar si ya hay compras asociadas a este producto.
    """
    producto = get_producto_by_gtin(gtin)
    elimina(producto)
    return redirect(url_for('productos.main'))


@productos.route('/change-status/<gtin>')
@requiere_inicio_sesion
def cambiar_status(gtin):
    """Elimina al producto. Soft Delete."""
    producto = get_producto_by_gtin(gtin)
    producto.status = not producto.status
    agrega(producto)
    flash("Producto cambiado con éxito")
    return redirect(url_for('productos.main'))


@productos.route('/crear-tipo-producto', methods=['POST', 'GET'])
@requiere_inicio_sesion
def create_tipo_producto():
    """Crea un nuevo tipo de producto si no existe."""
    if request.method == 'POST':
        body = request.json
        nombre_tipo_producto = body['nombre'].upper()

        if not get_tipo_by_nombre(nombre_tipo_producto):
            nuevo_tipo = TipoProducto(nombre_tipo_producto)
            agrega(nuevo_tipo)
            flash("Tipo creado correctamente")
        else:
            flash("Ya existe un tipo con este nombre")
    return render_template("cafeteria/productos/productos.html")


@productos.route('/crear-categoria', methods=['POST'])
@requiere_inicio_sesion
def create_categoria():
    """Crea una nueva categoria si no existe."""
    if request.method == 'POST':
        body = request.json  # ['body']
        nombre_categoria = body['nombre'].title()

        if not get_categoria_by_nombre(nombre_categoria):
            nueva_categoria = Categoria(nombre_categoria)
            agrega(nueva_categoria)
        else:
            flash("Ya existe una categoria con este nombre")
    return redirect(url_for('productos.main'))
