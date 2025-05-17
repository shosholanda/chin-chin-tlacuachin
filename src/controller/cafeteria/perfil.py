"""Controlador para la página de perfil.

"""
import math
from flask import (
    render_template, Blueprint, flash, redirect, request, url_for, session
)

from src.model.repository.repo import *
from src.model.entity.usuario import Usuario

from src.controller.auth import requiere_inicio_sesion
# Bibliotecas de seguridad
from werkzeug.security import generate_password_hash, check_password_hash

perfil = Blueprint('perfil', __name__, url_prefix='/perfil')


@perfil.route('/')
@requiere_inicio_sesion
def main():
    """Página principal de productos."""
    correo = session['usuario']
    usuario = get_by_id(Usuario, correo)
    return render_template('cafeteria/perfil/perfil.html', usuario=usuario)

# Cómo hacer para que se pueda ver otros perfiles?
# @perfil.route('<username>/', methods=['GET', 'POST'])
# @requiere_inicio_sesion
# def usuario(username):
#     """Página para visualizar solo un producto."""
#     usuario = get_by_id(Usuario, username)
#     if not usuario: 
#         return redirect(url_for('dashboard.main'))
#     return render_template('cafeteria/perfil/perfil.html', usuario=usuario)

@perfil.route('update', methods=['GET', 'POST'])
@requiere_inicio_sesion
def update():
    if request.method == 'POST':
        body = request.json
        nombre = body['nombre']
        apellido_paterno = body['apellido_paterno']
        apellido_materno = body['apellido_materno']
        fecha_nacimiento = body['fecha_nacimiento']

        fields = [nombre, apellido_materno, apellido_paterno, fecha_nacimiento]
        if None in fields:
            flash("Llena todos los campos por favor no seas tonoto")
        else:
            correo = session['usuario']
            usuario = get_by_id(Usuario, correo)
            if usuario == None:
                flash("No se puede actualizar a este usuario porque es None")
            else:
                usuario.nombre = nombre
                usuario.apellido_paterno = apellido_paterno
                usuario.apellido_materno = apellido_materno
                usuario.fecha_nacimiento = fecha_nacimiento
                agrega(usuario)
                flash("Se actualizó el usuario correctamente")

    return redirect(url_for('perfil.main'))

@perfil.route('delete')
@requiere_inicio_sesion
def deactivate():
    """Soft delete para no evitar registros."""
    correo = session['usuario']
    usuario = get_by_id(Usuario, correo)
    soft_delete(usuario)
    session.clear()
    return redirect(url_for('home'))
    # Puta perra madre porque no redirecciona
    # return redirect(url_for('auth.logout'))

@perfil.route('change-pwd/', methods=['GET', 'POST'])
@requiere_inicio_sesion
def change_pass():
    if request.method == 'POST':

        usuario = get_by_id(Usuario, session['usuario'])

        old_pwd = request.form.get('old-pwd')
        old_pwd2 = request.form.get('old-pwd2')
        new_pwd = request.form.get('new-pwd')

        if old_pwd2 != old_pwd:
            flash("Las contraseñas no coinciden")
        elif not(check_password_hash(usuario.contraseña, old_pwd) and check_password_hash(usuario.contraseña, old_pwd2)):
            flash("Contraseña no coincide con la contraseña previamente guardada.")
        else:
            usuario.contraseña = generate_password_hash(new_pwd)
            agrega(usuario)
            flash("Contraseña cambiada con éxito")
        
    return redirect(url_for('perfil.main'))



