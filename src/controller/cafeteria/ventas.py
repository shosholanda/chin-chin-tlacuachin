"""Controlador para efectuar ventas.

Todas las ventas requieren de productos para validarse.
"""
from flask import (
    render_template, Blueprint, flash, redirect, request, url_for, session
)

from src.model.dto.venta import Venta
from src.model.dto.transaccion import Transaccion
# from werkzeug.exceptions import abort

from src.model.repository.repo import agrega, elimina
from src.model.repository.repo_producto import *
from src.model.repository.repo_venta import *

# LMAO
from src.static.php.tickets.tools import create_php
import os

from src.controller.auth import requiere_inicio_sesion

ventas = Blueprint('ventas', __name__, url_prefix='/ventas')


@ventas.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de ventas."""
    ventas = get_all_ventas()[::-1]
    
    return render_template('cafeteria/ventas/base_venta.html',
                           ventas=ventas)


@ventas.route('/create-venta', methods=('GET', 'POST'))
@requiere_inicio_sesion
def create_venta():
    """Registra un venta con todos los datos en la base de datos."""
    if request.method == 'GET':
        return render_template('cafeteria/ventas/carrito.html')
    
    if request.method == 'POST':
        body = request.json
        # {'cart': [{'id_producto': 8, 'cantidad': 3}], 'total': '900', 'propina': '0', 'notas': '3', 'cliente': ''}
        
        nueva_venta = Venta(id_usuario=session['usuario'],
                            total=float(body['total']),
                            propina=float(body['propina']),
                            notas=body['notas'],
                            cliente=body['cliente']
                            )
        agrega(nueva_venta)
        ref = nueva_venta.referencia
        
        for c in body['cart']:
            transaccion = Transaccion(id_referencia=ref,
                                      id_producto=c['id_producto'],
                                      cantidad=c['cantidad']
                                      )
            agrega(transaccion)
        flash("Compra realizada")
            
    return redirect(url_for('ventas.main'))

@ventas.route('get-gtins/<pseudogtin>', methods=['GET'])
@requiere_inicio_sesion
def get_gtins(pseudogtin):
    """Obtiene los gtins que contengan en este orden el gtin."""
    gtins = get_subgtin_and_status(pseudogtin)
    return {'gtins': {x.gtin: f'{x.nombre} {x.categoria.nombre} {x.tipo_producto.nombre}' for x in gtins}}

@ventas.route('get-gtin/<gtin>', methods=["GET"])
@requiere_inicio_sesion
def get_gtin(gtin):
    producto = get_producto_by_gtin(gtin)
    return {'id': producto.id,
            'gtin': producto.gtin,
            'nombre': producto.nombre,
            'precio': producto.precio}

@ventas.route('get-transacciones-by-ref/<id_referencia>', methods=['GET'])
@requiere_inicio_sesion
def get_transactions_by_ref(id_referencia):
    transacciones = get_transacciones_by_ref(id_referencia)
    return [{'id_referencia': x.id_referencia,
             'producto': x.producto.nombre,
             'cantidad': x.cantidad} for x in gtins]


@ventas.route('/print-venta/<referencia>', methods=['GET'])
@requiere_inicio_sesion
def print_ticket(referencia):
    referencia = int(referencia)
    venta = get_venta_by_ref(referencia)
    trans = get_transaccion_by_ref(referencia)
    prods = [{'nombre': p.producto.nombre,
              'cantidad': p.cantidad,
              'precio': p.producto.precio} for p in trans]
    php = create_php(venta.cliente, prods, venta.total,
                     referencia, venta.fecha)
    file_path = os.path.expanduser('~/Downloads/tickets/ticket{:03d}.php'.format(referencia))
    f = open(file_path, 'w')
    f.write(php)
    f.close()
    return {'status': 'ok'}
    
    

@ventas.route('/eliminar-venta/<gtin>')
@requiere_inicio_sesion
def delete_venta(gtin):
    """Elimina el venta para siempre.

    No se puede eliminar si ya hay compras asociadas a este venta.
    """
    return redirect(url_for('ventas.main'))

