from flask import Blueprint, render_template
from flask import flash, render_template, request, redirect, url_for, session, current_app
from modules.utils import get_conn

user_app = Blueprint('user_app', __name__, static_folder="../static",
                      template_folder="../templates")

@user_app.route('/user/<nick>')
def user(nick):
    with current_app.app_context():
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