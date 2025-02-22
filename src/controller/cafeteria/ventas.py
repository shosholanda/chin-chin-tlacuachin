"""Controlador para efectuar ventas.

Todas las ventas requieren de productos para validarse.
"""
from flask import (
    render_template, Blueprint, flash, redirect, request, url_for, session, abort
)

from src.model.dto.venta import Venta
from src.model.dto.transaccion import Transaccion

from src.model.repository.repo import agrega, elimina
from src.model.repository.repo_producto import (
    get_subgtin_and_status, get_producto_by_gtin
)
from src.model.repository.repo_venta import (
    get_all_ventas, get_venta_by_ref, get_transaccion_by_ref
)

from src.static.php.tickets.ticket import Ticket

from src.controller.auth import requiere_inicio_sesion

ventas = Blueprint('ventas', __name__, url_prefix='/ventas/')


@ventas.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de ventas."""
    ventas = get_all_ventas()[::-1]
    return render_template('cafeteria/ventas/base_venta.html',
                           ventas=ventas)


@ventas.route('create-venta/', methods=('GET', 'POST'))
@requiere_inicio_sesion
def create_venta():
    """Registra un venta con todos los datos en la base de datos."""
    if request.method == 'POST':
        body = request.json
        # {'cart': [{'id_producto': 8, 'cantidad': 3}], 'total': '900', 'propina': '0', 'notas': '3', 'cliente': ''}

        cart = body['cart']
        if cart == []:
            flash("No hay productos para comprar.")
            return redirect(url_for('ventas.main'))
        nueva_venta = Venta(id_usuario=session['usuario'],
                            total=float(body['total']),
                            propina=float(body['propina']),
                            notas=body['notas'],
                            cliente=body['cliente']
                            )
        agrega(nueva_venta)

        for c in cart:
            transaccion = Transaccion(id_referencia=nueva_venta.referencia,
                                      id_producto=c['id_producto'],
                                      cantidad=c['cantidad']
                                      )
            agrega(transaccion)
        flash("¡Compra realizada! Anita mi amor <3")
        return redirect(url_for('ventas.main'))
    return render_template('cafeteria/ventas/carrito.html')


@ventas.route('/update-venta/<referencia>', methods=['POST'])
@requiere_inicio_sesion
def update_venta(referencia):
    """Actualiza los valores que no estan relacionados con otras tablas."""
    json = request.json
    venta = get_venta_by_ref(referencia)
    if not venta:
        flash("No se puede recuperar la venta " + referencia)
    else:
        venta.propina = json['propina']
        venta.notas = json['notas']
        venta.cliente = json['cliente']
        agrega(venta)
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
            'precio': producto.precio} if producto else None


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


@ventas.route('/print-venta/', methods=['POST'])
@requiere_inicio_sesion
def print_ticket():
    """Imprime el ticket de compra, con o sin RFC."""
    body = request.json

    referencia = body['referencia']
    rfc = body['rfc']
    venta = get_venta_by_ref(referencia)
    trans = get_transaccion_by_ref(referencia)
    prods = [{'nombre': p.producto.nombre,
              'cantidad': p.cantidad,
              'precio': p.producto.precio} for p in trans]

    ticket = Ticket(venta.cliente, prods, venta.total, referencia, rfc)
    response = {'status': ticket.print_ticket('/dev/usb/lp0')}

    return response


@ventas.route('/<referencia>')
@requiere_inicio_sesion
def referencia(referencia):
    """Muestra la información de una sola referencia."""
    venta = get_venta_by_ref(referencia)
    if not venta:
        abort(404)
    return render_template('cafeteria/ventas/referencia.html', venta=venta)


@ventas.route('/eliminar-venta/<referencia>')
@requiere_inicio_sesion
def delete_venta(referencia):
    """Elimina el venta para siempre."""
    transacciones = get_transaccion_by_ref(referencia)
    for t in transacciones:
        elimina(t)
    elimina(get_venta_by_ref(referencia))
    flash("Venta eliminada con éxito")
    return redirect(url_for('ventas.main'))
