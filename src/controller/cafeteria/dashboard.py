"""Controlador para la página de inicio principal de la cuenta."""
from flask import (
    render_template, Blueprint, session
)

from src.model.entity.usuario import Usuario
from src.model.repository.repo import *

from src.controller.auth import requiere_inicio_sesion


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@requiere_inicio_sesion
def main():
    """Método principal a ejecutar."""
    user = get_by_id(Usuario, session['usuario'])
    return render_template('cafeteria/dashboard.html', user=user)
