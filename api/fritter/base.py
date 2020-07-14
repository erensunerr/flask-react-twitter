from flask import (
    Blueprint, g, request, current_app, jsonify
)

from fritter.db import get_db

from fritter.auth import login_required

bp = Blueprint('base', __name__, url_prefix='/base')

@bp.route('/get_posts', methods=['POST'])
def get_posts():
    """Gets posts.

    :param post authors: optionally get posts belonging to multiple authors.
    :return: array of posts
    :rtype: JSON array
    """

    try:
        last_num = request.form['last_num']
    except:
        last_num = 0

    try:
        authors = list(request.form['authors'].replace(" ","").split(','))
        print(authors)
    except:
        authors = None

    db = get_db()
    if authors is not None:
        s = ('SELECT body, author, created, id FROM posts WHERE author IN ('+
             (', '.join(["?" for i in range(len(authors))]))+
             ')  ORDER BY created ASC LIMIT 15 OFFSET ?')
        posts = db.execute(s, tuple(authors + [last_num])).fetchall()
        print(posts)
    elif authors is None:
        posts = db.execute(
            'SELECT body, author, created, id FROM posts '
            'ORDER BY created ASC LIMIT 15 OFFSET ?', (last_num,)
        ).fetchall()

    q = []
    for post in posts:
        q += [{'body': post['body'],
               'author': post['author'],
               'created': post['created'],
               'id': post['id']
              }]

    return jsonify(q)


@bp.route('/delete_post', methods=['POST'])
@login_required
def delete_post():
    """Used to delete a post.

    :param post id: id of the post
    :return:  status (0 good, 1 bad, check docs for login_required)
    :rtype:  {'status': (int)}
    """
    db = get_db()
    if not request.form['id']:
        return {'status': 1}
    else:
        id = request.form['id']
    posts = db.execute(
        'DELETE FROM posts '
        'WHERE id == ? AND author == ?', (id, g.user['username'])
    )
    db.commit()
    return {'status': 0}



@bp.route('/create_post', methods=['POST'])
@login_required
def create_post():
    """Used to create a post.

    :param post body: supply a body text for this post
    :return: status (0 good, 1 bad, check docs for login_required)
    :rtype: {'status': (int)}
    """
    db = get_db()

    try:
        db.execute(
            'INSERT INTO posts (author, body) VALUES (?,?)',
            (g.user['username'], request.form['body'])
        )
        db.commit()
        return {'status': 0}
    except:
        return {'status': 1}
