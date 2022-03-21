import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

conn = sqlite3.connect('database.db',check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        session.pop('user', None)
        nick = request.form['nck']
        password = request.form['pswrd']
        email = request.form['eml']
        c.execute("INSERT INTO users (nick, password, email) VALUES (?, ?, ?)", (nick, password, email))
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
        print(nick)
        return render_template('user.html', nick=nick, email=email, password=password)
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
            print(data)
            session['user'] = {}
            session['user']['nick'] = data[1]
            session['user']['password'] = password
            session['user']['email'] = email
            return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == "POST":
        session.pop('user', None)
        return redirect(url_for('index'))
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
