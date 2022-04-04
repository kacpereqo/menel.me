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

    #TODO:
    # trzeba se jebnąc tutaj zeby nie robilo tych requestow za kazdym razem tylko np co 5 min 

    # if session.get('top_posts') is None:
    c.execute("SELECT posts.id ,posts.views, posts.title FROM posts ORDER BY posts.views DESC LIMIT 10")
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

        c.execute(
            "SELECT * FROM posts WHERE posts.user_id = ? ORDER BY posts.id DESC LIMIT 10", (user[0],))
        posts = c.fetchall()

        if os.path.isfile(os.path.join(current_app.root_path, 'static/img/avatars/' + str(user[0]) + '.webp')):
            id = '/static/img/avatars/' + str(user[0]) + '.webp'
        else:
            id = user[0]
            id = str(id)[len(str(id)) - 1]
            id = '/static/img/avatars_defaults/' + id + '.webp'

        return render_template('user.html', nick=user[1], email=user[3], password=user[2], id=user[0], posts=posts, avatar=id)

@user_app.route('/change_avatar/', methods=['POST', 'GET'])
def change_avatar():
    with current_app.app_context():
        if "user" in session:
            if request.method == 'POST':
                user_id = session['user']['id']
                file = request.files['file'].stream.read()

                avatar = Image.open(io.BytesIO(file)).convert('RGB')
                avatar.resize((128, 128), Image.LANCZOS).save('static/img/avatars/' + str(user_id) + '.webp', optimize=True, quality=30)
             
            return render_template('change_avatar.html')
        else:
            return redirect(url_for('index'))