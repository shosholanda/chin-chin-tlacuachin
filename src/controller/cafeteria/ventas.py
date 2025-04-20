"""Controlador para efectuar ventas.

Todas las ventas requieren de productos para validarse.
"""
from flask import (
    jsonify, render_template, Blueprint, flash, redirect, render_template_string, request, url_for, session, abort
)

from src.model.dto.venta import Venta
from src.model.dto.transaccion import Transaccion
from src.model.dto.tipo_pago import TipoPago

from src.model.repository.repo import *
from src.model.repository.repo_producto import get_subgtin_and_status, get_producto_by_gtin
from src.model.repository.repo_venta import get_transaccion_by_ref

from src.static.php.tickets.ticket import Ticket

from src.controller.auth import requiere_inicio_sesion

ventas = Blueprint('ventas', __name__, url_prefix='/ventas/')


@ventas.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de ventas."""
    ventas = get_all(Venta, limit=100)[::-1]
    return render_template('cafeteria/ventas/ventas.html',
                           ventas=ventas)


@ventas.route('create-venta/', methods=['POST'])
@requiere_inicio_sesion
def create_venta():
    """Registra un venta con todos los datos en la base de datos."""
    body = request.json
    # {'cart': [{'id_producto': 8, 'cantidad': 3}], 
    #  'total': '900', 
    #  'propina': '0', 
    #  'notas': 'algo', 
    #  'cliente': '',
    #  'tipo_pago': 1}

    cart = body['cart']
    print(body)
    if cart == []:
        flash("No hay productos para comprar.")
        return redirect(url_for('ventas.main')) 
    nueva_venta = Venta(id_usuario=session['usuario'],
                        id_tipo_pago=int(body['payment']),
                        total=float(body['total']),
                        propina=float(body['tip']),
                        notas=body['notes'],
                        cliente=body['client']
                        )
    agrega(nueva_venta)

    for c in cart:
        transaccion = Transaccion(id_referencia=nueva_venta.referencia,
                                    id_producto=c['product_id'],
                                    cantidad=c['quantity'])
        agrega(transaccion)
    flash("¡Compra realizada!")
    return redirect(url_for('ventas.main'))

@ventas.route('carrito/')
@requiere_inicio_sesion
def shopcar():
    """El carro donde se compran cosas"""
    tipo_pagos = [x for x in get_all_by_status(TipoPago)]
    return render_template('cafeteria/ventas/carrito.html', tipo_pagos=tipo_pagos)


@ventas.route('/update-venta/<referencia>', methods=['POST', 'GET'])
@requiere_inicio_sesion
def update_venta(referencia):
    """Actualiza los valores que no estan relacionados con otras tablas."""
    if request.method == 'POST':
        json = request.json
        venta = get_by_id(Venta, referencia)
        if not venta:
            flash("No se puede recuperar la venta " + referencia)
        else:
            venta.propina = json['propina']
            venta.notas = json['notas']
            venta.cliente = json['cliente']
            agrega(venta)
            flash("Se actualizó correctamente el producto!")
    return redirect(url_for('ventas.referencia', referencia=referencia))


@ventas.route('get-gtins/<pseudogtin>', methods=['GET'])
@requiere_inicio_sesion
def get_gtins(pseudogtin):
    """Obtiene los gtins que contengan en este orden el gtin."""
    gtins = get_subgtin_and_status(pseudogtin)
    return {'gtins': {x.gtin: f'{x.nombre} {x.categoria.nombre} {x.tipo_producto.nombre}' for x in gtins}}


@ventas.route('get-gtin/<gtin>', methods=["GET"])
@requiere_inicio_sesion
def get_gtin(gtin):
    """Obtiene un producto por GTIN."""
    producto = get_producto_by_gtin(gtin)
    return {'id': producto.id,
            'gtin': producto.gtin,
            'nombre': producto.nombre,
            'precio': producto.precio} if producto else {}


@ventas.route('get-transacciones-by-ref/<id_referencia>', methods=['GET'])
@requiere_inicio_sesion
def get_transactions_by_ref(id_referencia):
    """Obtiene todas las transacciones de una compra."""
    transacciones = get_transaccion_by_ref(id_referencia)
    if not transacciones:
        abort(401)
    return [{'id_referencia': x.id_referencia,
             'producto': x.producto.nombre,
             'cantidad': x.cantidad} for x in transacciones]


@ventas.route('print-venta/', methods=['POST'])
@requiere_inicio_sesion
def print_ticket():
    """Imprime el ticket de compra, con o sin RFC."""
    body = request.json

    referencia = body['referencia']
    rfc = body['rfc']
    venta = get_by_id(Venta, referencia)
    trans = get_transaccion_by_ref(referencia)
    prods = [{'nombre': p.producto.nombre,
              'cantidad': p.cantidad,
              'precio': p.producto.precio} for p in trans]

    ticket = Ticket(venta.cliente, prods, venta.total, referencia, rfc)
    response = {'status': ticket.print_ticket('/dev/usb/lp0')}

    return response

@ventas.route('get-item/<gtin>&<int:cantidad>')
@requiere_inicio_sesion
def get_item_layout(gtin, cantidad):
    producto = get_gtin(gtin)
    if not producto:
        flash("El producto no existe!")
        return {}

    producto['cantidad'] = cantidad
    producto['subtotal'] = cantidad * float(producto['precio'])
    html = """
        {% import 'macro.html' as mc %}
        {{- mc.create_item(producto) }}
    """
    html = render_template_string(html, producto = producto)
    producto['html'] = html
    return producto


@ventas.route('<referencia>/')
@requiere_inicio_sesion
def referencia(referencia):
    """Muestra la información de una sola referencia."""
    venta = get_by_id(Venta, referencia)
    if not venta:
        return redirect(url_for('ventas.main'))
    return render_template('cafeteria/ventas/referencia.html', venta=venta)


@ventas.route('delete-venta/<referencia>')
@requiere_inicio_sesion
def delete_venta(referencia):
    """Elimina el venta para siempre."""
    transacciones = get_transaccion_by_ref(referencia)
    for t in transacciones:
        elimina(t)
    elimina(get_by_id(Venta, referencia))
    flash("Venta eliminada con éxito")
    return redirect(url_for('ventas.main'))
