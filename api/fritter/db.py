import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """Short summary.

    :return: Description of returned object.
    :rtype: type
    :raises ExceptionName: Why the exception is raised.

    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Short summary.

    :param type e: Description of parameter `e`.
    :return: Description of returned object.
    :rtype: type
    :raises ExceptionName: Why the exception is raised.

    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Short summary.

    :return: Description of returned object.
    :rtype: type
    :raises ExceptionName: Why the exception is raised.

    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Short summary.

    :return: Description of returned object.
    :rtype: type
    :raises ExceptionName: Why the exception is raised.

    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Short summary.

    :param type app: Description of parameter `app`.
    :return: Description of returned object.
    :rtype: type
    :raises ExceptionName: Why the exception is raised.

    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
