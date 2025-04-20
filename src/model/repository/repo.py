"""Consultas en general para poder reutilizar."""
from src import db


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


def get_by_name(model, name, all=False):
    """Regresa el registro que coincida con el modelo y con el nombre."""
    if has_column(model, 'nombre'):
        if all:
            return model.query.filter(model.nombre == name).all()
        return model.query.filter(model.nombre == name).first()
    return []


def get_by(column, model, identifier, all=False):
    """Funcion para regresar los registros de cierta columna de cierta tabla."""
    pass


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

