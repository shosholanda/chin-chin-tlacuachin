"""Tabla de usuarios."""
from src import db


class Usuario(db.Model):
    """Clase que mapea un usuario a un registro en la bdd.

    Entidad: Usuario
    Los usuarios son los que operan el punto de venta, ya sea compra,
    venta o administración.
    """

    __tablename__ = 'usuario'
    correo = db.Column('correo', db.String(100), primary_key=True)
    nombre = db.Column('nombre', db.String(100), nullable=False)
    apellido_paterno = db.Column('apellido_paterno', db.String(100), nullable=False)
    apellido_materno = db.Column('apellido_materno', db.String(100), nullable=False)
    contraseña = db.Column('contraseña', db.String(162), nullable=False)
    fecha_nacimiento = db.Column('fecha_nacimiento', db.Date, nullable=False)
    status = db.Column('status', db.Boolean, default=1, nullable=False)

    ventas = db.relationship('Venta', back_populates='usuario')

    def __init__(self, correo, contraseña, nombre, apellido_paterno,
                 apellido_materno, fecha_nacimiento):
        """Create a new row."""
        self.correo = correo
        self.contraseña = contraseña
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.fecha_nacimiento = fecha_nacimiento

    def __repr__(self):
        """Representación en cadena de este objeto."""
        return f'{self.correo}\t{self.nombre}\t{self.fecha_nacimiento}'
    
    def full_name(self):
        """Nombre completo."""
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'
