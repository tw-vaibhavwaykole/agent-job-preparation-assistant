from flask import current_app, g
from flask_login import current_user
from functools import wraps

def get_db():
    if 'db' not in g:
        g.db = current_app.db.session
    return g.db

def get_current_user():
    return current_user

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return {'error': 'Authentication required'}, 401
        return f(*args, **kwargs)
    return decorated 