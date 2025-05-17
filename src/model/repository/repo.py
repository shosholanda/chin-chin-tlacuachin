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


def get_by_name(model, name, column='nombre', all=False):
    """Regresa el registro que coincida con el modelo y con el nombre."""
    if get_column(model, column) is not None:
        if all:
            return model.query.filter(model.nombre.contains(name)).all()
        return model.query.filter(model.nombre == name).first()
    return []

def get_first(model):
    return db.session.query(model).first()


def get_by_fecha(model, ini=None, fin=None, column='fecha'):
    """Obtiene registros por fecha [a, b]"""
    if get_column(model, column) is None:
        return []
    if not ini:
        first = get_first(model)
        ini = first.fecha
    if not fin:
        fin = dt.date.today()
    return model.query\
        .filter(model.fecha >= ini)\
        .filter(model.fecha <= fin)


def sum_column(model, column, query=None):
    """Suma todos los valores que puedan sumarse."""
    if not has_column(model, column):
        return 0
    col = getattr(model.__table__.columns, column)
    if query is None:
        return db.session.query(func.sum(col)).scalar()
    else:
        query = query.subquery()
        subq = query.c[column] if hasattr(query, 'c') else col
        return db.session.query(func.sum(subq)).select_from(query).scalar() or 0

def get_all(model, limit:int=None, offset:int=None, order:str='ASC', column:str=None, status=False):
    """Regresa todos los registros de este modelo."""
    query = model.query
    if has_column(model, 'status'):
        if status:
            query = query.filter(model.status == 1)
    if column:
        col = getattr(model.__table__.columns, column)
        if order == 'DESC':
            query = query.order_by(col.desc())
        else:
            query = query.order_by(col.asc())
        
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    return query.all()
    
def count_rows(model, status=False):
    """Cuenta cuantas filas tiene esta tabla."""
    query = db.session.query(model)
    if has_column(model, 'status'):
        if status:
            return query.filter(model.status == 1).count()
    return db.session.query(model).count()


def get_column(model, name):
    """Funcion auxiliar que para saber si existe la columna en el modelo."""
    try:
        return getattr(model.__table__.columns, name)
    except AttributeError:
        return None
    
def has_column(model, column):
    return hasattr(model.__table__.columns, column)

