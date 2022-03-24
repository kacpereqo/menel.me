from flask import g
import sqlite3
from datetime import timedelta

def get_conn():
    DATABASE = 'data\db\database.sqlite'
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE)
    return conn

def config(app):
    from modules.login import login_app
    from modules.post import post_app
    app.secret_key = "secret"
    app.permanent_session_lifetime = timedelta(minutes=5)
    app.register_blueprint(login_app)
    app.register_blueprint(post_app)
    return app