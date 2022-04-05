from flask import Blueprint, render_template
from flask import flash, render_template, request, redirect, url_for, session, current_app
from modules.utils import get_conn
from datetime import datetime
from PIL import Image
import io

post_app = Blueprint('post_app', __name__, static_folder="../static",
                     template_folder="../templates")


@post_app.before_request
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
    

@post_app.route("/create", methods=['POST', 'GET'])
def create():
    with current_app.app_context():
        if "user" in session:
            if request.method == 'POST':
                title = request.form['title']
                description = request.form['description']
                content = request.files['file'].stream.read()

                if len(content) < 1:
                    flash("Plik nie może być pusty")
                    return redirect(url_for('post_app.create'))
                if len(title) < 1:
                    flash("Tytuł nie może być pusty")
                    return redirect(url_for('post_app.create'))
                if len(description) < 1:
                    flash("Opis nie może być pusty")
                    return redirect(url_for('post_app.create'))

                conn = get_conn()
                c = conn.cursor()

                c.execute("SELECT title FROM posts WHERE title = ?", (title,))

                if c.fetchone() is not None:
                    flash("Post z taką nazwą już istnieje!")
                    return redirect(url_for('post_app.create'))

                if request.form['file_type'] == "zdjecie":
                    try:
                        image = Image.open(io.BytesIO(content)).convert('RGB')
                    except:
                        flash("Niepoprawny format obrazka")
                        return redirect(url_for('post_app.create'))

                    latest_id = get_conn().execute(
                        "SELECT seq FROM sqlite_sequence where name='posts'").fetchone()[0]

                    image.resize((130, 100), Image.LANCZOS).save('static/img/posts/' + str(latest_id) + '_small.webp', optimize=True, quality=35)
                    image.save('static/img/posts/' + str(latest_id) + '_large.webp', optimize=True, quality=60) # kurwa w cs poszedlem grac
                    image.save('static/img/posts/' + str(latest_id) + '_original.webp', optimize=True, quality=60) # po chui jest large i original?
                    # guwniarzu po to że huj wiem co robi ale nie wiem co to jest, ale działa, ale nie wiem jak to zrobić lepiej, ~github copilot

                    # how to find grilfriend
                    # c.execute("SELECT id FROM users WHERE username = ?", (session['user'],))
                    # user_id = c.fetchone()[0]
                
                    user_id = session['user']['id']
                    date = datetime.now()

                    conn = get_conn()
                    c = conn.cursor()

                    c.execute("INSERT INTO posts (title, description, img_id, user_id, date)VALUES (?, ?, ?, ?, ?)",
                              (title, description, latest_id, user_id, date))
                    conn.commit()

                if request.form["file_type"] == "film":
                    # tak
                    pass

                flash("Dodano post!")
                return redirect(url_for('index'))
            return render_template('create.html')
        else:
            return redirect(url_for('index'))


@post_app.route("/post_lookup/<post_id>")
def post_lookup(post_id):
    with current_app.app_context():
        conn = get_conn()
        c = conn.cursor()
        c.execute("UPDATE posts SET views = views + 1 WHERE id = ?", (post_id,))
        conn.commit()
        c.execute(
            "SELECT users.nick, posts.date, posts.title, posts.img_id, posts.description, posts.id, posts.upvotes,posts.downvotes, posts.views   FROM posts,users WHERE posts.id = ? and posts.user_id = users.id", (post_id,))
        post = c.fetchone()
        c.execute("SELECT users.nick,comments.date,comments.content FROM comments,users WHERE comments.post_id = ? and comments.user_id = users.id ORDER BY comments.date", (post_id,))
        comments = c.fetchall()
        print(comments)
        return render_template('post_lookup.html', post=post, comments=comments)


@post_app.route("/upvote/<post_id>")
def upvote(post_id):
    with current_app.app_context():
        conn = get_conn()
        c = conn.cursor()
        c.execute("UPDATE posts SET upvotes = upvotes + 1 WHERE id = ?", (post_id,))
        conn.commit()
        return redirect(url_for('post_app.post_lookup', post_id=post_id))


@post_app.route("/downvote/<post_id>")
def downvote(post_id):
    with current_app.app_context():
        conn = get_conn()
        c = conn.cursor()
        c.execute(
            "UPDATE posts SET downvotes = downvotes + 1 WHERE id = ?", (post_id,))
        conn.commit()
        return redirect(url_for('post_app.post_lookup', post_id=post_id))


@post_app.route("/comment/<post_id>", methods=['POST', 'GET'])
def comment(post_id):
    with current_app.app_context():
        if "user" in session:
            if request.method == 'POST':
                user_id = session['user']['id']

                comment = request.form['comment']
                date = datetime.now()

                conn = get_conn()
                c = conn.cursor()

                c.execute("INSERT INTO comments (content, user_id, post_id, date)VALUES (?, ?, ?, ?)",
                          (comment, user_id, post_id, date))
                conn.commit()
                flash("Dodano komentarz!")
                return redirect(url_for('post_app.post_lookup', post_id=post_id))
            return render_template('comment.html', post_id=post_id)
        else:
            return redirect(url_for('index'))

