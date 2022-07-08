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
def admin_panel():
    if "user" in session:
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT permission FROM users WHERE id = ?", (session["user"]['id'],))
        if c.fetchone()[0] < 2:
            flash("Nie masz uprawnień do tej strony!")
            return redirect(url_for('index'))
    else:
        flash("Nie masz uprawnień do tej strony!")
        return redirect(url_for('index'))

    return render_template("admin.html")

@admin_app.route('/admin/unban', methods=['GET', 'POST'])
def unban():
    if "user" in session:
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT permission FROM users WHERE id = ?", (session["user"]['id'],))
        if c.fetchone()[0] < 2:
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
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT permission FROM users WHERE id = ?", (session["user"]['id'],))
        if c.fetchone()[0] < 2:
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

            conn = get_conn()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE nick = ? OR email = ?", (user_nick, user_email))

            data = c.fetchone()

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

@admin_app.route('/admin/permissions', methods=['GET', 'POST'])
def permissions():
    perm = [False]
    if "user" in session:
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT permission FROM users WHERE id = ?", (session["user"]['id'],))
        if c.fetchone()[0] < 2:
            flash("Nie masz uprawnień do tej strony!")
            return redirect(url_for('index'))
    else:
        flash("Nie masz uprawnień do tej strony!")
        return redirect(url_for('index'))

    with current_app.app_context():
        if request.method == 'POST':

            user_nick = request.form['nick']
            user_email = request.form['email']

            conn = get_conn()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE nick = ? OR email = ?", (user_nick, user_email))

            data = c.fetchone()

            print(data)

            if data is None:
                flash("Nie ma takiego użytkownika!")
                return render_template('permissions.html', perm=perm)

            if request.form['smb'] == "Sprawdz":
                c.execute("SELECT nick,permission FROM users WHERE id = ?", (data[0], ))
                t = c.fetchone()
                perm = [True,t[0],t[1]]
                return render_template('permissions.html', perm=perm)

            if request.form['smb'] == "Zmien":

                c.execute("SELECT nick,permission FROM users WHERE id = ?", (data[0], ))
                t = c.fetchone()
                c.execute("UPDATE users SET permission = ? WHERE id = ?", (request.form['permiss'], data[0]))
                conn.commit()
                flash(f"Uprawnienia dla {t[0]} zostały zmienione na poziom {request.form['permiss']} z {t[1]}")
                perm = [False]
                return render_template('permissions.html', perm=perm)
            
        return render_template('permissions.html', perm=perm)

@admin_app.route('/admin/remove_post', methods=['GET', 'POST'])
def remove_post():
    if "user" in session:
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT permission FROM users WHERE id = ?", (session["user"]['id'],))
        if c.fetchone()[0] < 2:
            flash("Nie masz uprawnień do tej strony!")
            return redirect(url_for('index'))
    else:
        flash("Nie masz uprawnień do tej strony!")
        return redirect(url_for('index'))

    with current_app.app_context():
        if request.method == 'POST':

            conn = get_conn()
            c = conn.cursor()
            c.execute("SELECT * FROM posts WHERE id = ?", (request.form['id_post'],))

            data = c.fetchone()

            if data is None:
                flash("Nie ma takiego posta!")
                return render_template('remove_post.html')

            if request.form['smb'] == "Usun":
                c.execute("DELETE FROM posts WHERE id = ?", (str(data[0]), ))
                flash("Post został usunięty!")
                return render_template('remove_post.html')
                
        return render_template('remove_post.html')
    

@admin_app.route('/report/<nick>/<int:post_id>', methods=['GET', 'POST'])
def report(nick, post_id):
    # if request method post
    #  if "user" in session:
    #     conn = get_conn()
    #     c = conn.cursor()
    #     c.execute("SELECT permission FROM users WHERE id = ?", (session["user"]['id'],))
    #     if c.fetchone()[0] != 2:
    #         flash("Nie masz uprawnień do tej strony!")
    #         return redirect(url_for('index'))
    # else:
    #     flash("Nie masz uprawnień do tej strony!")
    #     return redirect(url_for('index'))
    if request.method == 'POST':
        if "user" not in session:
            flash("Najpierw musisz się zalogować!")
            return redirect(url_for('index'))
        
        if (len(request.form['reason']) - request.form['reason'].count(" ")) < 1:
            flash("Zgłosznie nie może być puste")
            return render_template('report.html', nick=nick, post_id=post_id)       

        conn = get_conn()
        c = conn.cursor()
        flash("Zgłoszono użytkownika")
        with conn:
            c.execute("INSERT INTO reports (user_id, reason, post_id) VALUES (?, ?, ?)", (nick, "Zgłosznie autorstwa: "+ session["user"]["nick"] + " - " + request.form['reason'],post_id))
        return redirect(url_for('index'))
    # if request method get
    else:
        return render_template('report.html', nick=nick, post_id=post_id)        
