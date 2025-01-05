"""Controlador para la página de inicio principal de la cuenta."""
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from src.model.repository.repo_usuario import get_usuario

from src.controller.auth import requiere_inicio_sesion


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@requiere_inicio_sesion
def main():
    """Método principal a ejecutar."""
    user = get_usuario(g.user.correo)
    if not user:
        user = 'persona extraña'
    return render_template('cafeteria/dashboard.html', usuario=user)
