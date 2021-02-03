import sqlite3

import click
#g es un objeto unico para cada request se usa para almacenar datos que seran usados por varias funciones
#current_app es un apuntador a la aplicacion responsable del request (no es necesario con el patron de factory?)
from flask import current_app, g
from flask.cli import with_appcontext

def init_app(app):
    #Esto llama a la funcion close_db despues de enviar la respuesta
    app.teardown_appcontext(close_db)
    #Agrega un comando que puede ejecutarse con "flask X"
    app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #La bd devuelve las filas en formato dict con la siguiente lineas
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#Ejecuta consola
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')