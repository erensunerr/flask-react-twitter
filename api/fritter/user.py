from flask import (
    Blueprint, g, request, current_app
)

from fritter.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/get_posts')
@login_required
def get_posts():
    """will give you posts.
    ::
    :return: Description of returned object.
    :rtype: type
    :raises ExceptionName: Why the exception is raised.

    """
