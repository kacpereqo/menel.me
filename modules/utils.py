from flask import g
import sqlite3
from datetime import timedelta

def get_conn():
    DATABASE = 'db/database.sqlite'
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE)
    return conn

def config(app):
    from modules.login import login_app
    from modules.post import post_app
    from modules.user import user_app
    with app.app_context():
        app.secret_key = "rot13"
        app.permanent_session_lifetime = timedelta(minutes=5)
        app.register_blueprint(login_app)
        app.register_blueprint(post_app)
        app.register_blueprint(user_app)
        app.config['MAX_CONTENT_LENGTH'] = 128 * 1000 * 1000
    return app