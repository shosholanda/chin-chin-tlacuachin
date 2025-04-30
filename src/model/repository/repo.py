"""Consultas en general para poder reutilizar."""
from src import db
from sqlalchemy import func
import datetime as dt


def agrega(objeto):
    """Agrega un objeto (fila) a la base de datos.

    El objeto ya sabe cómo se mapea a la tabla por el ORM.
    """
    db.session.add(objeto)
    db.session.commit()


def elimina(objeto):
    """Elimina a esta 'fila' de la base de datos.

    El objeto ya sabe cómo se mapea a la tabla por el ORM.
    """
    db.session.delete(objeto)
    db.session.commit()


def soft_delete(objeto):
    """Efectua un soft-delete para este objeto, si tiene status."""
    if objeto.status:
        if objeto.status == 1:
            objeto.status = 0
            agrega(objeto)


def get_by_id(model, id):
    """Regresa el registro que coincida con el modelo y con el id."""
    return model.query.get(id)


def get_by_name(model, name, col_name='nombre', all=False):
    """Regresa el registro que coincida con el modelo y con el nombre."""
    if has_column(model, col_name):
        if all:
            return model.query.filter(model.nombre.contains(name)).all()
        return model.query.filter(model.nombre == name).first()
    return []

def get_first(model):
    return db.session.query(model).first()


def get_by_fecha(model, ini=None, fin=None, col_name='fecha'):
    """Obtiene registros por fecha [a, b]"""
    if not has_column(model, col_name):
        return []
    if not ini:
        first = get_first(model)
        ini = first.fecha
    if not fin:
        fin = dt.date.today()
    return model.query\
        .filter(model.fecha >= ini)\
        .filter(model.fecha <= fin)


def sum_column(model, col_name, query=None):
    """Suma todos los valores que puedan sumarse."""
    if not has_column(model, col_name):
        return 0
    col = getattr(model.__table__.columns, col_name)
    if query is None:
        return db.session.query(func.sum(col)).scalar()
    else:
        subq = query.c[col_name] if hasattr(query, 'c') else col
        return db.session.query(func.sum(subq)).select_from(query).scalar() or 0

def get_all(model, limit=None):
    """Regresa todos los registros de este modelo."""
    if limit:
        return model.query.limit(limit).all()
    return model.query.all()


def get_all_by_status(model):
    """Regresa todos los registros de este modelo que tengan status = 1.
    
    Si no se tiene la columna status, se toman todas las filas como status = 1."""
    if has_column(model, 'status'):
        return model.query.filter(model.status == 1).all()
    else:
        return get_all(model)


def has_column(model, name):
    """Funcion auxiliar que para saber si existe la columna en el modelo."""
    for c in model.__table__.columns:
        if name in str(c):
            return True
    return False

