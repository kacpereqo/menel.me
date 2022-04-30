from turtle import st
from flask import Blueprint, render_template
from flask import flash, render_template, request, redirect, url_for, session, current_app
from sqlalchemy import true
from modules.utils import get_conn
import os
import io
from PIL import Image

user_app = Blueprint('user_app', __name__, static_folder="../static",
                     template_folder="../templates")


@user_app.before_request
def before_request_func():
    conn = get_conn()
    c = conn.cursor()

    # TODO:
    # trzeba se jebnąc tutaj zeby nie robilo tych requestow za kazdym razem tylko np co 5 min

    # if session.get('top_posts') is None:
    c.execute(
        "SELECT posts.id ,posts.views, posts.title FROM posts ORDER BY posts.views DESC LIMIT 10")
    top_posts = c.fetchall()
    # session['top_posts'] = top_posts

    c.execute("SELECT posts.id ,posts.img_id FROM posts ORDER BY RANDOM() LIMIT 1")
    post = c.fetchone()
    current_app.jinja_env.globals.update(random=post, top_posts=top_posts)


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

        else:
            c.execute(f"SELECT posts.id, posts.date, posts.img_id, posts.title, posts.views, posts.upvotes, posts.downvotes  FROM posts where posts.user_id = ? ORDER BY posts.id", (user[0],))
            posts = c.fetchall()

            points = 0
            for post in posts:
                points += (post[5] - post[6])*10 + post[4]

            if os.path.isfile(os.path.join(current_app.root_path, 'static/img/avatars/' + str(user[0]) + '.webp')):
                avatar_path = '/static/img/avatars/' + str(user[0]) + '.webp'
            else:
                avatar_path = str(user[0])[len(str(user[0])) - 1]
                avatar_path = '/static/img/avatars_defaults/' + avatar_path + '.webp'

        if user[4] == False:
            return render_template('user.html', nick=user[1], banned=True, reason=user[5])

        return render_template('user.html', nick=user[1], avatar=avatar_path, last_login=user[8], date_created=user[7], banned=False, description=user[9], posts=posts,points=points)


@user_app.route('/change_avatar/', methods=['POST', 'GET'])
def change_avatar():
    with current_app.app_context():
        if "user" in session:
            if request.method == 'POST':
                user_id = session['user']['id']
                content = request.files['file'].stream.read()

                try:
                    avatar = Image.open(io.BytesIO(content)).convert('RGB')
                except:
                    flash("Niepoprawny format pliku!")
                    return render_template('change_avatar.html')

                if avatar.size[0] < 128 or avatar.size[1] < 128:
                    flash("Za mały rozmiar zdjęcia!")
                    return redirect(url_for('user_app.change_avatar'))

                avatar.resize((128, 128), Image.LANCZOS).save(
                    'static/img/avatars/' + str(user_id) + '.webp', optimize=True, quality=30)
                flash("Avatar został zmieniony!")
                return redirect(url_for('user_app.user', nick=session['user']['nick']))
            return render_template('change_avatar.html')
        else:
            flash("Musisz być zalogowany!")
            return redirect(url_for('index'))

# @user_app.route('/change_description/', methods=['POST', 'GET'])
# def change_description():
#     with current_app.app_context():
#         if "user" in session:
#             if request.method == 'POST':
#                 user_id = session['user']['id']
#                 description = request.form['description']


@user_app.route('/settings/', methods=['POST', 'GET'])
def settings():
    with current_app.app_context():
        if "user" in session:
            if request.method == 'POST':
                user_id = session['user']['id']
                password = request.form['password']
                email = request.form['email']

                conn = get_conn()
                c = conn.cursor()

                c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                user = c.fetchone()

                if user[2] != password:
                    flash("Niepoprawne hasło!")
                    return redirect(url_for('user_app.settings'))

                c.execute("UPDATE users SET email = ? WHERE id = ?",
                          (email, user_id))
                conn.commit()

                flash("Dane zostały zmienione!")
                return redirect(url_for('user_app.user', nick=session['user']['nick']))
            return render_template('settings.html')
        else:
            flash("Musisz być zalogowany!")
            return redirect(url_for('index'))
