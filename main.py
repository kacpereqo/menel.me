# co tu to robi kurwa!?!?!?!??! xddddddddddddddddddddddddddddddddddddddddddddddddddd
from urllib import response
from flask import Flask, make_response, render_template, request, redirect, url_for, session, flash
# from flask_caching import Cache
from modules.utils import config, get_conn
from datetime import datetime, timedelta
import base64
from wtforms import Form, BooleanField, StringField, PasswordField, validators
app = config(Flask(__name__))


@app.route('/')
def index():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT posts.id, users.nick, posts.date, posts.img_id  FROM posts,users where posts.user_id = users.id ORDER BY posts.id DESC LIMIT 10")
    posts = c.fetchall()
    response = make_response(render_template('index.html', posts=posts))
    return response


@app.route('/user/<nick>')
def user(nick):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE nick = ?", (nick,))
    user = c.fetchone()

    if user is None:
        flash("Użytkownik nie istnieje!")
        return redirect(url_for('index'))

    c.execute(
        "SELECT * FROM posts WHERE posts.user_id = ? ORDER BY posts.id DESC LIMIT 10", (user[0],))
    posts = c.fetchall()

    return render_template('user.html', nick=user[1], email=user[3], password=user[2], id=user[0], posts=posts)

# +48 69 69 69 69 call me later <3 :3


if __name__ == '__main__':
    app.run(debug=True)
# smierc ma haslo sex123 nie arek123

# lihrjpnoszghyqjk
