import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """Loads the database into g.

    :return: g.db
    :rtype: sqlite3.connect()
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Offloads the database from g and closes the database.

    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Creates the database using the provided schema.sql file.

    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """The command line version of the function init_db, call it with 'init-db'.
    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Makes sure the db gets closed and init-db command works.

    :param type app: flask.Flask.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
