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
    return render_template("admin.html")