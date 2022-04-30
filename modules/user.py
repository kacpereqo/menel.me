from turtle import st
from flask import Blueprint, render_template
from flask import flash, render_template, request, redirect, url_for, session, current_app
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
            # count
            c.execute("SELECT COUNT(*) FROM posts WHERE user_id = ?", (user[0],))
            post_count = c.fetchall()

            if os.path.isfile(os.path.join(current_app.root_path, 'static/img/avatars/' + str(user[0]) + '.webp')):
                avatar_path = '/static/img/avatars/' + str(user[0]) + '.webp'
            else:
                avatar_path = str(user[0])[len(str(user[0])) - 1]
                avatar_path = '/static/img/avatars_defaults/' + avatar_path + '.webp'

        return render_template('user.html', user=user, avatar=avatar_path, post_coutn=post_count)


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
