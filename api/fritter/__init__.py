import os
from flask import Flask
from fritter import db
from fritter import auth
from fritter import base
def create_app():
    """Application factory.

    :return: the application.
    :rtype: flask.Flask
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fritter.sqlite')
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from fritter import db
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(base.bp)

    return app
