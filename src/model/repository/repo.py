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
            db.session.add(objeto)
            db.session.commit()
