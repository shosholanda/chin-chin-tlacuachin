"""Consultas con la tabla de articulo."""
from src.model.dto.articulo import Articulo
from src.model.dto.tipo_articulo import TipoArticulo


def get_all_articulos():
    """Regresa todas las filas de articulo."""
    return Articulo.query.all()


def get_all_tipo_articulos():
    """Regresa todas las filas del tipo_articulo."""
    return TipoArticulo.query.all()


def get_tipo_articulo_by_name(name):
    """Regresa el tipo articulo que coinicida con nombre."""
    return TipoArticulo.query.filter(TipoArticulo.nombre == name).first()


def get_articulo_by_id(id_articulo):
    """Regresa el articulo por id."""
    return Articulo.query.get(id_articulo)


def get_articulo_by_nombre(nombre):
    """Regresa el/los articulo/s con el nombre especificado."""
    return Articulo.query.filter(Articulo.nombre == nombre).first()


def get_insumo_by_nombre(insumo):
    """Regresa el articulo que esta marcado como insumo."""
    id_insumo = get_tipo_articulo_by_name('INSUMO').id
    return get_subarticulo_and_status(insumo).filter(Articulo.id_tipo_articulo == id_insumo).all()


def get_subarticulo(pseudoarticulo):
    """Regresa los articulos que contengan el código gtin."""
    return Articulo.query.filter(Articulo.nombre.contains(pseudoarticulo))


def get_subarticulo_and_status(subarticulo):
    """Regresa los articulos activos que contengan subarticulo."""
    return get_subarticulo(subarticulo).filter(Articulo.status == 1)
