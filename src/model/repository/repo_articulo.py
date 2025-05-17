"""Consultas con la tabla de articulo."""
from src.model.entity.articulo import Articulo
from src.model.entity.tipo_articulo import TipoArticulo
from src.model.repository.repo import get_by_name


def get_insumo_by_nombre(insumo):
    """Regresa el articulo que esta marcado como insumo."""
    id_insumo = get_by_name(TipoArticulo, 'INSUMO').id
    return get_subarticulo_and_status(insumo).filter(Articulo.id_tipo_articulo == id_insumo).all()


def get_subarticulo(pseudoarticulo):
    """Regresa los articulos que contengan el código gtin."""
    return Articulo.query.filter(Articulo.nombre.contains(pseudoarticulo))


def get_subarticulo_and_status(subarticulo):
    """Regresa los articulos activos que contengan subarticulo."""
    return get_subarticulo(subarticulo).filter(Articulo.status == 1)
