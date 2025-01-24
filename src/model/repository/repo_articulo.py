"""Consultas con la tabla de articulo."""
from src.model.dto.articulo import Articulo


def get_all_articulos():
    """Regresa todas las filas de articulo."""
    return Articulo.query.all()


def get_articulo_by_id(id_articulo):
    """Regresa el articulo por id."""
    return Articulo.query.get(id_articulo)


def get_articulo_by_nombre(nombre):
    """Regresa el/los articulo/s con el nombre especificado."""
    return Articulo.query.filter(Articulo.nombre == nombre).first()


def get_articulo_by_gtin(gtin):
    """Regresa el articulo con el gtin especificado."""
    return Articulo.query.filter(Articulo.gtin == gtin).first()


def get_subarticulo(pseudoarticulo):
    """Regresa los articulos que contengan el código gtin."""
    return Articulo.query.filter(Articulo.gtin.contains(pseudoarticulo))


def get_subarticulo_and_status(subarticulo):
    """Regresa los articulos activos que contengan subarticulo."""
    return get_subarticulo(subarticulo).filter(Articulo.status == 1)
