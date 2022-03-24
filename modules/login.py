from flask import Blueprint, render_template
from flask import flash, render_template, request, redirect, url_for, session, current_app
from modules.utils import get_conn
from argon2 import PasswordHasher 
from argon2.exceptions import VerifyMismatchError

login_app = Blueprint('login_app', __name__, static_folder="../static",
                  template_folder="../templates")           
ph = PasswordHasher()
    
@login_app.route('/login', methods=['POST', 'GET'])
def login(): 
    with current_app.app_context():

        conn = get_conn()
        c = conn.cursor()

        if request.method == 'POST':
            email = request.form['eml']
            password = request.form['pswrd']

            password = ph.hash(password)

            c.execute(
                "SELECT * FROM users WHERE email = ?", (email,))
            data = c.fetchone()

            if data is None:
                return redirect(url_for('index'))
            else:
                try:
                    isValid = ph.verify(password, data[1])
                except VerifyMismatchError:
                    isValid = False
                if isValid:
                    session['user'] = {}
                    session['user']['nick'] = data[1]
                    session['user']['password'] = data[2]
                    session['user']['email'] = email
                    session['user']['id'] = data[0]
                    flash(f'Zalogowano pomyślnie jako {data[1]}')
                    return redirect(url_for('user', nick=data[1]))
        return redirect(url_for('index'))


@login_app.route('/register', methods=['POST', 'GET'])
def register():
    with current_app.app_context():

        conn = get_conn()
        c = conn.cursor()

        if request.method == 'POST':
            session.pop('user', None)
            nick = request.form['nck']
            password = request.form['pswrd']
            email = request.form['eml']

            # trzeba walidowac emaile nicki i hasla czy maja dlugosc znaki itp
            # co tam wariacie, odpisz mi

            password = ph.hash(password)

            c.execute("INSERT INTO users (nick, password, email) VALUES (?, ?, ?)",
                    (nick, password, email))
            conn.commit()
            flash("Zarejestrowano pomyślnie!")
            return redirect(url_for('login'))
        return render_template('register.html')


@login_app.route('/logout', methods=['POST', 'GET'])
def logout():
     with current_app.app_context():

        conn = get_conn()
        c = conn.cursor()
        session.pop('user', None)
        flash('Wylogowano pomyślnie!')
        return redirect(url_for('index'))
