"""Controlador para registrar y logearse."""
import functools

from flask import (render_template, Blueprint, flash, g, redirect,
                   request, session, url_for)

# Bibliotecas de seguridad
from werkzeug.security import generate_password_hash, check_password_hash
# Crear automáticamente las tablas en mysql
from src.model.dto.usuario import Usuario
# Importar las querys requeridas
from src.model.repository.repo import *

# Crear el endpoint y lo registra
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/registrar-usuario', methods=['GET', 'POST'])
def registrar_usuario():
    """Registra a un usuario en la aplicación WEB."""
    if request.method == 'POST':
        correo = request.form.get('email')
        contraseña = request.form.get('password')
        nombre = request.form.get('name')
        apellido_paterno = request.form.get('first-name')
        apellido_materno = request.form.get('last-name')
        fecha_nacimiento = request.form.get('birthday')
        fields = [correo, contraseña, nombre, apellido_paterno,
                    apellido_materno, fecha_nacimiento]

        if None in fields:
            flash("Rellena todos los campos por favor")
            return render_template('auth/register.html')

        nombre = nombre.strip().title()
        apellido_paterno = apellido_paterno.strip().title()
        apellido_materno = apellido_materno.strip().title()
        msg_flash = None

        usuario_bdd = get_by_id(Usuario, correo)
        if not usuario_bdd:
            user = Usuario(correo=correo,
                           contraseña=generate_password_hash(contraseña),
                           nombre=nombre,
                           apellido_paterno=apellido_paterno,
                           apellido_materno=apellido_materno,
                           # id_tipo_usuario=1,
                           # id_sucursal=None,
                           fecha_nacimiento=fecha_nacimiento)
            agrega(user)
            flash('Cuenta creada con éxito. Ahora inicia sesión')
            return redirect(url_for('auth.iniciar_sesion'))
        elif not usuario_bdd.status:
            msg_flash = 'Cuenta desactivada.'
        else:
            msg_flash = 'Usuario ya existe'
        flash(msg_flash)
    return render_template('auth/register.html')


# Iniciar sesion
@auth.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    """Inicia sesión verificando que exista el correo y la contraseña."""
    if request.method == 'POST':
        correo = request.form.get('email')
        contraseña = request.form.get('password')

        msg_flash = None
        if not correo or not contraseña:
            msg_flash = "Escriba un usuario y contraseña"

        usuario_bdd = get_by_id(Usuario, correo)
        if not usuario_bdd:
            msg_flash = "Usuario no existe"
        elif not check_password_hash(usuario_bdd.contraseña, contraseña):
            msg_flash = 'Usuario o contraseña incorrecta'
        elif not usuario_bdd.status:
            msg_flash = 'Cuenta de usuario suspendida'

        if not msg_flash:
            session.clear()
            session['usuario'] = usuario_bdd.correo
            # session['tipo_usuario'] = usuario_bdd.tipo_usuario.nombre
            # if usuario_bdd.sucursal:
            # session['sucursal'] = user.sucursal.nombre
            return redirect(url_for('dashboard.main'))
        flash(msg_flash)
    return render_template('auth/login.html')


@auth.before_app_request
def cargar_usuarios_logeados():
    """Antes de cada petición se obtiene la información de inicio se sesión."""
    usuario = session.get('usuario')
    if usuario:
        g.user = get_by_id(Usuario, usuario)
    else:
        g.user = None

@auth.route('/cerrar-sesion')
def logout():
    """Termina la sesión y limpia el registro de usuario."""
    session.clear()
    return redirect(url_for('home'))


def requiere_inicio_sesion(vista):
    """Requiere que se haya iniciado sesión al usar este decorador.

    Aplica para los usuarios registrados en la página, no personas públicas.
    """
    @functools.wraps(vista)
    def wrapper(*args, **kwargs):
        if not g.user:
            return redirect(url_for('home'))
        return vista(*args, **kwargs)
    return wrapper
