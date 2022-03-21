import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_caching import Cache
from datetime import datetime, timedelta
import base64

conn = sqlite3.connect('database.sqlite', check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.secret_key = "secret"
app.permanent_session_lifetime = timedelta(minutes=5)

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/')
@cache.cached(timeout=300)
def index():
    c.execute("SELECT * FROM posts,users where posts.user_id = users.id ORDER BY posts.id DESC LIMIT 10")
    posts = c.fetchall()
    return render_template('index.html', posts=posts)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        session.pop('user', None)
        nick = request.form['nck']
        password = request.form['pswrd']
        email = request.form['eml']
        c.execute("INSERT INTO users (nick, password, email) VALUES (?, ?, ?)",
                  (nick, password, email))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/user/<nick>')
def user(nick):
    c.execute("SELECT * FROM users WHERE nick = ?", (nick,))
    user = c.fetchone()
    return render_template('user.html', nick=user[1], email=user[3], password=user[2], id = user[0])


# +48 69 69 69 69 call me later <3 :3

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['eml']
        password = request.form['pswrd']
        c.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        data = c.fetchone()
        if data is None:
            return redirect(url_for('index'))
        else:
            session['user'] = {}
            session['user']['nick'] = data[1]
            session['user']['password'] = password
            session['user']['email'] = email
            session['user']['id'] = data[0]
            return redirect(url_for('user'))
    return render_template('register.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


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
            c.execute("INSERT INTO posts (title, description, content, user_id, date)VALUES (?, ?, ?, ?, ?)",
                      (title, description, content, user_id, date))
            conn.commit()
            return redirect(url_for('index'))
        return render_template('create.html')
    else:
        return redirect(url_for('index'))

@app.route("/post_lookup/<post_id>")
def post_lookup(post_id):
    c.execute("SELECT * FROM posts,users WHERE posts.id = ? and posts.user_id = users.id", (post_id,))
    post = c.fetchone()
    return render_template('post_lookup.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)

#nikker test