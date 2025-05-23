"""Inicialización del proyecto.

Desde aquí creamos la aplicacion de flask, configuramos algunas cosas
de la base de datos como login, debug, controladores, base de datos etc
"""
# Aplicacion Flask
from flask import Flask
# SQL conexiones
from flask_sqlalchemy import SQLAlchemy
# Migraciones
from flask_migrate import Migrate

# Se crea una aplicación flask con el main de este programa
app = Flask(__name__)

# Configurar la aplicacion desde el objeto
app.config.from_object("config.DeveloperConfig")

# Cargar base de datos especificada en app
db = SQLAlchemy(app)
# inicializar flask migrate
migrate = Migrate(app, db)

# Cargar controladores entre bdd y vista
from src.controller.auth import auth
app.register_blueprint(auth)
from src.controller.cafeteria.dashboard import dashboard
app.register_blueprint(dashboard)
from src.controller.cafeteria.ventas import ventas
app.register_blueprint(ventas)
from src.controller.cafeteria.productos import productos
app.register_blueprint(productos)
from src.controller.cafeteria.gastos import gastos
app.register_blueprint(gastos)
from src.controller.cafeteria.inventario import inventario
app.register_blueprint(inventario)
from src.controller.cafeteria.perfil import perfil
app.register_blueprint(perfil)
from src.controller.cafeteria.reportes import reportes
app.register_blueprint(reportes)

# Crear las tablas de la aplicacion que siguen los modelos de esta
# aplicacion flask
with app.app_context():
    db.create_all()
