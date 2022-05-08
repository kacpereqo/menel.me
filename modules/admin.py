import secrets
import yagmail
from flask import Blueprint, render_template
from flask import flash, render_template, request, redirect, url_for, session, current_app
from modules.utils import get_conn

admin_app = Blueprint('admin_app', __name__, static_folder="../static",
                      template_folder="../templates")

@admin_app.before_request
def before_request_func():
    conn = get_conn()
    c = conn.cursor()

    #TODO:
    # trzeba se jebnąc tutaj zeby nie robilo tych requestow za kazdym razem tylko np co 5 min 

    # if session.get('top_posts') is None:
    c.execute("SELECT posts.id ,posts.views, posts.title FROM posts ORDER BY posts.views DESC LIMIT 10")
    top_posts = c.fetchall()
        # session['top_posts'] = top_posts

    c.execute("SELECT posts.id ,posts.img_id FROM posts ORDER BY RANDOM() LIMIT 1")
    post = c.fetchone()
    current_app.jinja_env.globals.update(random=post, top_posts=top_posts)

@admin_app.route("/admin")
def admin():
    if "user" in session:
        if session['user']['id'] != 1:
            flash("Nie masz uprawnień do tej strony!")
            return redirect(url_for('index'))
    else:
        flash("Nie masz uprawnień do tej strony!")
        return redirect(url_for('index'))

    return render_template("admin.html")

@admin_app.route('/admin/unban', methods=['GET', 'POST'])
def unban():
    if "user" in session:
        if session['user']['id'] != 1:
            flash("Nie masz uprawnień do tej strony!")
            return redirect(url_for('index'))
    else:
        flash("Nie masz uprawnień do tej strony!")
        return redirect(url_for('index'))

    with current_app.app_context():
        if request.method == 'POST':
            user_nick = request.form['nick']
            user_email = request.form['email']
            reason = ""

            conn = get_conn()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE nick = ? OR email = ?", (user_nick, user_email))

            data = c.fetchone()
            
            if data is None:
                flash("Nie ma takiego użytkownika!")
                return render_template('unban.html')
            else:
                token = secrets.token_urlsafe(16)
                
                c.execute("UPDATE users SET token = ? WHERE id = ?", (token, data[0]))
                conn.commit()
                c.execute("UPDATE users SET active = 1 WHERE id = ?", (data[0],))
                conn.commit()
                c.execute("UPDATE users SET reason = ? WHERE id = ?", (reason,data[0]))
                conn.commit()

                with yagmail.SMTP("meneleme.noreply@gmail.com", "lihrjpnoszghyqjk") as yag:
                    yag.send(data[3], "Konto odblokowane", ["Hejka "+data[1],"\n",
                            "<style>p {font-family: \"Comic Sans MS\", \"Comic Sans\", cursive;}</style><h3><p>Twoje konto zostało odblokowane!</p><h3>","\n","Pozdrawiamy, załoga menele.me B)"])

                flash("Gagatek zostal odbanowany")
                return render_template('unban.html')
                
        return render_template('unban.html')

@admin_app.route('/admin/ban', methods=['GET', 'POST'])
def ban():
    if "user" in session:
        if session['user']['id'] != 1:
            flash("Nie masz uprawnień do tej strony!")
            return redirect(url_for('index'))
    else:
        flash("Nie masz uprawnień do tej strony!")
        return redirect(url_for('index'))

    with current_app.app_context():
        if request.method == 'POST':
            user_nick = request.form['nick']
            user_email = request.form['email']
            reason = request.form['reason']

            print(user_nick, user_email, reason)

            conn = get_conn()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE nick = ? OR email = ?", (user_nick, user_email))

            data = c.fetchone()
            print(data)

            if data is None:
                flash("Nie ma takiego użytkownika!")
                return render_template('ban.html')
            else:
                token = secrets.token_urlsafe(16)
                
                c.execute("UPDATE users SET token = ? WHERE id = ?", (token, data[0]))
                conn.commit()
                c.execute("UPDATE users SET active = 0 WHERE id = ?", (data[0],))
                conn.commit()
                c.execute("UPDATE users SET reason = ? WHERE id = ?", (reason,data[0]))
                conn.commit()

                with yagmail.SMTP("meneleme.noreply@gmail.com", "lihrjpnoszghyqjk") as yag:
                    yag.send(data[3], "Konto zablokowane", ["Hejka "+data[1],"\n",
                            "<style>p {font-family: \"Comic Sans MS\", \"Comic Sans\", cursive;}</style><h3><p>Twoje konto zostało zablokowane!</p><h3>","\n","<p>Powód: "+reason+"</p>"])

                flash("Gagatek zostal zbanowany hehehehe")
                return render_template('ban.html')
                
        return render_template('ban.html')