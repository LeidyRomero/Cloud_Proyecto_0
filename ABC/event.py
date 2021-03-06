from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, make_response
)
from werkzeug.exceptions import abort

from ABC.auth import login_required
from ABC.db import get_db

bp = Blueprint('evento', __name__)

#-------------------------------------------VISTAS--------------------------------------
@bp.route('/index')
@login_required
def index():
    if g.user is None:
        autor=request.cookies.get('autor')
    else:
        autor=g.user['id']

    db = get_db()
    eventos = db.execute(
        'SELECT p.id, created, author_id, nombre, fechaInicial, Username'
        ' FROM evento p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?'
        ' ORDER BY created DESC',(autor,)
    ).fetchall()
    return render_template('evento/index.html', eventos=eventos)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        lugar = request.form['lugar']
        direccion = request.form['direccion']
        fechaInicial = request.form['fechaInicial']
        fechaFinal = request.form['fechaFinal']
        tipo = request.form['tipo']

        print(request.cookies.get('autor'))
        if g.user is None:
            autor=request.cookies.get('autor')
        else:
            autor=g.user['id']

        error = None
        print(fechaInicial)
        print(autor)
        if not nombre:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO evento (nombre, categoria, lugar, direccion, tipo, fechaInicial, fechaFinal, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (nombre, categoria, lugar, direccion, tipo, fechaInicial, fechaFinal, autor)
            )
            db.commit()
            return redirect(url_for('evento.index'))

    return render_template('evento/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    evento = get_evento(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        lugar = request.form['lugar']
        direccion = request.form['direccion']
        fechaInicial = request.form['fechaInicial']
        fechaFinal = request.form['fechaFinal']
        tipo = request.form['tipo']
        error = None

        if not nombre:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE evento SET nombre = ?, categoria = ?, lugar = ?, direccion = ?, fechaInicial = ?, fechaFinal = ?, tipo = ?'
                ' WHERE id = ?',
                (nombre, categoria, lugar, direccion, fechaInicial, fechaFinal, tipo, id)
            )
            db.commit()
            return redirect(url_for('evento.index'))

    return render_template('evento/update.html', evento=evento)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_evento(id)
    db = get_db()
    db.execute('DELETE FROM evento WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('evento.index'))
#-------------------------------------------FUNCIONES--------------------------------------
def get_evento(id, check_author=True):
    evento = get_db().execute(
        'SELECT p.id, created, author_id, nombre, categoria,lugar,direccion,tipo, Username'
        ' FROM evento p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if evento is None:
        abort(404, "Event id {0} doesn't exist.".format(id))

    if g.user is None:
        autor=request.cookies.get('autor')
    else:
        autor=g.user['id']

    if check_author and evento['author_id'] != autor:
        abort(403)

    return evento

@bp.route('/eventos/<int:id>/', methods=('GET',))
@login_required
def detail(id):
    db = get_db()
    evento = db.execute(
        'SELECT p.id, created, author_id, nombre, categoria, lugar, direccion, fechaInicial, fechaFinal, tipo, Username'
        ' FROM evento p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',(id,)
    ).fetchone()
    return render_template('evento/detail.html',evento=evento)
