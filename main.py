import logging
from functools import wraps

from flask import Flask, request, Response
from werkzeug.contrib.atom import AtomFeed
from librus import LibrusSession

import hashlib


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    # return username and password  # anything non-empty, this will be passed through
    session = LibrusSession()
    try:
        session.login(username, password)
        return True
    except RuntimeError:
        return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


app = Flask(__name__)


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/announcements')
@requires_auth
def announcements():
    session = LibrusSession()
    session.login(request.authorization.username, request.authorization.password)

    feed = AtomFeed("Announcements", feed_url=request.url, url=request.url_root)
    for announcement in session.list_announcements():
        feed.add(title=announcement.title,
                 content=render_announcement(announcement),
                 id=announcement_id(announcement),
                 content_type='text',
                 author=announcement.author,
                 url='https://synergia.librus.pl/ogloszenia',
                 updated=announcement.date,
                 published=announcement.date)
    return feed.get_response()


def render_announcement(announcement):
    rendered = '''Text:
-------------------------------------------
{content}
-------------------------------------------
'''.format(content=announcement.content)
    for attr in ('title', 'author', 'date'):
        rendered += '\n{k}: {v}'.format(k=attr, v=getattr(announcement, attr))
    return rendered


def announcement_id(announcement):
    hash = hashlib.sha256()
    for attr in sorted(attr for attr in dir(announcement) if attr[0] != '_'):
        hash.update(attr.encode('utf-8'))
        hash.update(str(getattr(announcement, attr)).encode('utf-8'))
    return hash.hexdigest()


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
