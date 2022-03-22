from urllib import response # co tu to robi kurwa!?!?!?!??!
from flask import Flask, make_response, render_template, request, redirect, url_for, session
# from flask_caching import Cache
from modules.utils import config, get_conn
from datetime import datetime, timedelta
import base64
from wtforms import Form, BooleanField, StringField, PasswordField, validators
app = config(Flask(__name__))

# config = {
#     "DEBUG": True,
#     "CACHE_TYPE": "SimpleCache",
#     "CACHE_DEFAULT_TIMEOUT": 300
# }
# app.config.from_mapping(config)
# cache = Cache(app)


@app.route('/')
def index():
    conn = get_conn()
    c = conn.cursor()
        
    c.execute("SELECT * FROM posts,users where posts.user_id = users.id ORDER BY posts.id DESC LIMIT 10")
    posts = c.fetchall()
    # mozna jebnac do tego osobna funkcje bo pierdolca idzie dostac xd
    # w sensie co?
    response = make_response(render_template('index.html', posts=posts))
    # response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/user/<nick>')
def user(nick):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE nick = ?", (nick,))
    user = c.fetchone()
    return render_template('user.html', nick=user[1], email=user[3], password=user[2], id=user[0])

# +48 69 69 69 69 call me later <3 :3

@app.route("/create", methods=['POST', 'GET'])
def create():
    if "user" in session:
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            content = base64.b64encode(
                request.files['file'].stream.read()).decode("utf-8")
            user_id = session['user']['id']
            date = datetime.now()

            conn = get_conn()
            c = conn.cursor()

            c.execute("INSERT INTO posts (title, description, content, user_id, date)VALUES (?, ?, ?, ?, ?)",
                      (title, description, content, user_id, date))
            conn.commit()
            return redirect(url_for('index'))
        return render_template('create.html')
    else:
        return redirect(url_for('index'))


@app.route("/post_lookup/<post_id>")
def post_lookup(post_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM posts,users WHERE posts.id = ? and posts.user_id = users.id", (post_id,))
    post = c.fetchone()
    return render_template('post_lookup.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)

# smierc ma haslo sex123 nie arek123
