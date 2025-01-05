"""Controlador para registrar y logearse."""
import functools

from flask import (render_template, Blueprint, flash, g, redirect,
                   request, session, url_for)

# Bibliotecas de seguridad
from werkzeug.security import generate_password_hash, check_password_hash
# Crear automáticamente las tablas en mysql
from src.model.dto.usuario import Usuario
# Importar las querys requeridas
from src.model.repository.repo_usuario import get_usuario
from src.model.repository.repo import agrega

# Crear el endpoint y lo registra
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/registrar-usuario', methods=['GET', 'POST'])
def registrar_usuario():
    """Registra a un usuario en la aplicación WEB."""
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        fecha_nacimiento = request.form.get('fecha_de_nacimiento')

        if None in [correo, contraseña, nombre, apellido_paterno,
                    apellido_materno, fecha_nacimiento]:
            flash("Rellena todos los campos por favor")
            return render_template('auth/register.html')

        nombre = nombre.strip().title()
        apellido_paterno = apellido_paterno.strip().title()
        apellido_materno = apellido_materno.strip().title()
        msg_flash = None

        usuario_bdd = get_usuario(correo)
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
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        msg_flash = None
        if not correo or not contraseña:
            msg_flash = "Escriba un usuario y contraseña"

        usuario_bdd = get_usuario(correo)
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
    return render_template('auth/login.html')


@auth.before_app_request
def cargar_usuarios_logeados():
    """Antes de cada petición se obtiene la información de inicio se sesión."""
    usuario = session.get('usuario')
    g.user = get_usuario(usuario)


@auth.route('/cerrar-sesion')
def cerrar_sesion():
    """Termina la sesión y limpia el registro de usuario."""
    session.clear()
    return redirect(url_for('home'))


def requiere_inicio_sesion(vista):
    """Requiere que se haya iniciado sesión al usar este decorador.

    Aplica para los usuarios registrados en la página, no personas públicas.
    """
    @functools.wraps(vista)
    def wrapper(**kwargs):
        if not g.user:
            return redirect(url_for('home'))
        return vista(**kwargs)
    return wrapper
