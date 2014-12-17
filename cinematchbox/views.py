"""
    cinematchbox

    This project allows users to create libraries of rated movies
    for the purpose of deciding what films to view as a group.

    The content is very heavily based off of the Flask tutorial (flaskr)
    and templates provided by bootstrap.

"""

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
from cinematchbox import app

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/')
def show_home():
    db = get_db()
    cur = db.execute('select title, description from movies order by id desc')
    movies = cur.fetchall()
    return render_template('index.html', movies=movies)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        print 'not logged in'
        abort(401)
    db = get_db()
    db.execute('insert into movies (title, description) values (?, ?)',
                 [request.form['title'], request.form['description']])
    db.commit()
    flash('New movie was successfully saved')
    return redirect(url_for('show_home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_home'))
    return render_template('bootstrap_signin.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_home'))


if __name__ == '__main__':
    init_db()
    app.run()
