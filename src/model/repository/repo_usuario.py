"""Consultas con la tabla de usuario."""
from src.model.dto.usuario import Usuario


def get_usuario(correo):
    """Obtiene el usuario por correo."""
    return Usuario.query.get(correo)


def get_usuarios_activos():
    """Obtiene usuarios con status = 1."""
    return Usuario.filter(Usuario.status == 1)
