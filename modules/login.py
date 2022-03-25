import re
import secrets
import yagmail
from flask import Blueprint, render_template
from flask import flash, render_template, request, redirect, url_for, session, current_app
from modules.utils import get_conn
import bcrypt
import validators

login_app = Blueprint('login_app', __name__, static_folder="../static",
                      template_folder="../templates")

@login_app.route('/login', methods=['POST', 'GET'])
def login():
    with current_app.app_context():

        conn = get_conn()
        c = conn.cursor()

        if request.method == 'POST':
            email = request.form['eml']
            password = request.form['pswrd']

            c.execute(
                "SELECT * FROM users WHERE email = ?", (email,))
            data = c.fetchone()

            if data is None:
                flash(f'Konto nie istnieje!')
                return redirect(url_for('index'))
                
            else:
                isValid = bcrypt.checkpw(password.encode('utf-8'), data[2].encode('utf-8'))

                print("valid: ", isValid)

                if int(data[4]) == 0 and isValid:
                    if len(data[5]) > 1:
                        flash(f"Konto zablokowane!\n{data[5]}")
                    else:
                        flash(f'Konto nie zostało aktywowane!') 
                    return redirect(url_for('index'))

                if int(data[4]) == 1 and isValid:
                    
                    session['user'] = {}
                    session['user']['nick'] = data[1]
                    session['user']['password'] = data[2]
                    session['user']['email'] = email
                    session['user']['id'] = data[0]
                    flash(f'Zalogowano pomyślnie jako {data[1]}')
                    return redirect(url_for('user', nick=data[1]))

                if isValid == False:
                    flash(f'Nieprawidłowe hasło!')
                    return redirect(url_for('index'))
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
            password_second = request.form['pswrd-r']
            email = request.form['eml']
            active = 0
            token = secrets.token_urlsafe(16)
            reason = ""

            if len(nick) < 3 and len(nick) > 20:
                flash(f'Nick musi mieć od 3 do 20 znaków!')
                return render_template('register.html', reason=reason)

            if not validators.email(email):
                flash(f'Nieprawidłowy adres email!')
                return render_template('register.html', reason=reason)

            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if(regex.search(nick) != None):
                flash(f'Nick nie może zawierać znaków specjalnych!')
                return render_template('register.html', reason=reason)   

            if len(password) < 10 and len(password) > 32:
                flash(f'Hasło musi mieć od 10 do 32 znaków!')
                return render_template('register.html', reason=reason)    

            if password != password_second:
                flash(f'Hasła nie są identyczne!')
                return render_template('register.html', reason=reason)

            c.execute("SELECT * FROM users WHERE nick = ?", (nick,))
            conn.commit()
            data = c.fetchone()

            if data is not None:
                flash(f'Nick jest zajęty!')
                return render_template('register.html', reason=reason)

            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            conn.commit()
            data = c.fetchone()

            if data is not None:
                flash(f'Email jest zajęty!')
                return render_template('register.html', reason=reason)

            verify_link = f"http://localhost:5000/verify?email={email}&token={token}"

            with yagmail.SMTP("meneleme.noreply@gmail.com", "lihrjpnoszghyqjk") as yag:
                yag.send(email, "Zweryfikuj konto", [
                         nick,"\n","Zweryfikuj konto na menele.me.","\n", verify_link,"\n","Pozdrawiamy, załoga menele.me B)"])

            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            password = password.decode('utf-8')

            c.execute("INSERT INTO users (nick, password, email, active, reason, token) VALUES (?, ?, ?, ?, ?, ?)",
                      (nick, password, email, active, reason, token))
            conn.commit()

            flash("Zarejestrowano pomyślnie! Zweryfikuj swoje konto")
            return redirect(url_for('login_app.login'))
        return render_template('register.html')


@login_app.route('/verify', methods=['POST', 'GET'])
def verify():
    email = request.args.get('email')
    token = request.args.get('token')

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT token,reason FROM users WHERE email = ?", (email,))
    conn.commit()

    token_from_db = c.fetchone()[0]

    # jest problem ze jak gosciu ma bana to moze sie odbanowac linkiem aktywacyjnym xd to nizej ma to blokowac ale cos nie dziala potem sie to naprawi xd

    # try:
    #     if len(c.fetchone()[1]) > 1:
    #         is_banned = True
    # finally:
    #     is_banned = False

    # if is_banned:
    #     flash(f"Konto zablokowane!\n{c.fetchone()[1]}")
    #     return redirect(url_for('index'))

    if token_from_db == token:
        c.execute("UPDATE users SET active = 1 WHERE email = ?", (email,))
        conn.commit()
        flash("Konto zostało aktywowane!")
    return redirect(url_for('login_app.login'))

@login_app.route('/reset_password', methods=['POST', 'GET'])
def reset_password():

    # email = request.args.get('email')
    # token = request.args.get('token')

    # with current_app.app_context():
    #     if request.method == 'POST':
    #         # reset password
    #         email = request.form['email']
    #         token = secrets.token_urlsafe(16)
    #         reason = ""

    #         if not validators.email(email):
    #             flash(f'Nieprawidłowy adres email!')
    #             return render_template('reset_password.html', reason=reason)
            
    #         conn = get_conn()
    #         c = conn.cursor()
    #         c.execute("SELECT * FROM users WHERE email = ?", (email,))
    #         conn.commit()
    #         data = c.fetchone()

    #         verify_link = f"http://localhost:5000/reset_password?email={email}&token={token}"
            
    #         with yagmail.SMTP("meneleme.noreply@gmail.com", "lihrjpnoszghyqjk") as yag:
    #             yag.send(email, "Reset hasła", )


            


        return render_template('reset_password.html')


@login_app.route('/logout', methods=['POST', 'GET'])
def logout():
    with current_app.app_context():

        conn = get_conn()
        c = conn.cursor()
        session.pop('user', None)
        flash('Wylogowano pomyślnie!')
        return redirect(url_for('index'))