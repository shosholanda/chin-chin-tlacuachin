"""Controlador para efectuar ventas.

Todas las ventas requieren de productos para validarse.
"""
from flask import (
    render_template, Blueprint, flash, redirect, render_template_string, request, url_for, session, abort
)

from src.model.entity.venta import Venta
from src.model.entity.transaccion import Transaccion
from src.model.entity.tipo_pago import TipoPago

from src.model.repository.repo import *
from src.model.repository.repo_producto import get_subgtin_and_status, get_producto_by_gtin
from src.model.repository.repo_venta import *

from src.static.php.tickets.ticket import Ticket

from src.controller.auth import requiere_inicio_sesion
import datetime as dt

ventas = Blueprint('ventas', __name__, url_prefix='/ventas/')


@ventas.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de ventas."""
    page = request.args.get(key='page', default=1, type=int)
    paginacion= 10
    start = (page-1) * paginacion
    end = start + paginacion
    total = count_rows(Venta)//paginacion
    ventas = get_all(Venta, limit=paginacion, offset=start, order='DESC', column='referencia')
    return render_template('cafeteria/ventas/ventas.html',
                           ventas=ventas, page=page, total=total)

@ventas.route('fecha/', methods=['GET'])
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
    ventas = get_by_fecha(Venta, ini, fin)
    if filter != 'NaN':
        ventas = ventas.join(Venta.tipo_pago).filter(TipoPago.id == filter)
    payment = get_by_id(TipoPago, filter)
    total = sum_column(Venta, 'total', ventas)
    return render_template('cafeteria/ventas/tabla.html', ventas=ventas, payment=payment, total=total)


@ventas.route('periodo/', methods=['GET'])
@requiere_inicio_sesion
def periodo():
    """Visualiza las últimas ventas realizadas en el periodo timespan"""
    today = dt.date.today()
    timespan = request.args.get('period', 'day', str)
    ini = fin = today
    if timespan == 'day':
        pass
    elif timespan == 'week':
        ini = (dt.datetime.now() - dt.timedelta(days=7)).date()
    elif timespan == 'month':
        ini = (dt.datetime.now() - dt.timedelta(days=30)).date()

    payments = get_all(TipoPago) + [None]
    return render_template('cafeteria/ventas/periodo.html', timespan=timespan, filter=payments,
                           ini=ini, fin=fin)


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
    tipo_pago = int(body['payment']) if body['payment'] != None else None
    total = float(body['total'])
    propina = float(body['tip'])
    notas = body['notes']
    cliente = body['client']

    nueva_venta = Venta(id_usuario=session['usuario'],
                        id_tipo_pago=tipo_pago,
                        total=total,
                        propina=propina,
                        notas=notas,
                        cliente=cliente
                        )
    agrega(nueva_venta)

    for c in cart:
        transaccion = Transaccion(id_referencia=nueva_venta.referencia,
                                    id_producto=c['product_id'],
                                    cantidad=c['quantity'])
        agrega(transaccion)
    flash("¡Compra realizada!" )
    if tipo_pago:
        return redirect(url_for('ventas.main'))
    else:
        return redirect(url_for('ventas.referencia', referencia=nueva_venta.referencia))

@ventas.route('carrito/')
@requiere_inicio_sesion
def shopcar():
    """El carro donde se compran cosas"""
    tipo_pagos = [x for x in get_all(TipoPago, status=1)]
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
            venta.id_tipo_pago = json['tipo_pago'] if json['tipo_pago'] != "" else None
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
    return render_template('cafeteria/ventas/referencia.html', venta=venta, tipo_pagos= get_all(TipoPago))


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
