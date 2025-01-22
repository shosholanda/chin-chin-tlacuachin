"""Punto de partida del punto de venta."""
from src import app
# from livereload import Server

from flask import (render_template, redirect, g, url_for)


@app.route('/')
def home():
    """Página pública."""
    if g.user:
        return redirect(url_for('dashboard.main'))
    return render_template('home.html')


def get_object_server():
    """Regresa la aplicacion como un objeto."""
    return app


if __name__ == '__main__':
    app.run()
    # server = Server(app.wsgi_app)
    # server.serve(port=5000)
