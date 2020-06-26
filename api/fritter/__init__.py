import os
from flask import Flask
from fritter import db
from fritter import auth

def create_app():
    """Short summary.

    :return: Description of returned object.
    :rtype: type
    :raises ExceptionName: Why the exception is raised.

    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello!"

    from fritter import db
    db.init_app(app)


    app.register_blueprint(auth.bp)

    app.add_url_rule('/', endpoint='index')

    return app
