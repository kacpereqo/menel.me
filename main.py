import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import base64

conn = sqlite3.connect('database.sqlite', check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.secret_key = "secret"


@app.route('/')
def index():
    # 10 latest posts
    c.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 10")
    posts = c.fetchall()
    return render_template('index.html',posts = posts)


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


@app.route('/user')
def user():
    if "user" in session:
        user = session['user']
        nick = user['nick']
        email = user['email']
        password = user['password']
        user_id = user['id']
        return render_template('user.html', nick=nick, email=email, password=password, id = user_id)
    else:
        return redirect(url_for('index'))


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
    return render_template('login.html')


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
            content = base64.b64encode(request.files['file'].stream.read()).decode("utf-8")
            user_id = session['user']['id']
            date = datetime.now()
            c.execute("INSERT INTO posts (title, description, content, user_id,date)VALUES (?, ?, ?, ?, ?)",
                      (title, description, content, user_id, date))
            conn.commit()
            return redirect(url_for('index'))
        return render_template('create.html')
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
