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
    from modules.admin import admin_app
    with app.app_context():
        app.secret_key = "rot13"
        app.permanent_session_lifetime = timedelta(minutes=10)
        app.register_blueprint(login_app)
        app.register_blueprint(post_app)
        app.register_blueprint(user_app)
        app.register_blueprint(admin_app)
        # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 7200
        app.config['MAX_CONTENT_LENGTH'] = 32 * 1000 * 1000
        app.config['SESSION_PERMANENT'] = False
        app.config['USE_SESSION_FOR_NEXT'] = False
        app.config['SESSION_PROTECTION'] = 'strong'
    return app

def cleanFilename(s,  r =" %:/,.\\[]<>*?"):
    return ''.join([c for c in s if c not in r])