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
                content_raw = request.files['file']
                content = content_raw.stream.read()

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
                        i = Image.open(io.BytesIO(content)).convert('RGB')
                    except:
                        flash("Niepoprawny format obrazka")
                        return redirect(url_for('post_app.create'))

                    latest_id = get_conn().execute(
                        "SELECT seq FROM sqlite_sequence where name='posts'").fetchone()[0]

                    i.resize((130, 100), Image.LANCZOS).save('static/img/posts/' + str(latest_id) + '_small.webp', optimize=True, quality=35)

                    image_watermark = Image.open('static/img/logo.png').convert('RGBA')

                    scale = 0.3

                    image_watermark = image_watermark.resize((round((i.size[0]/i.size[1])*311*scale),round((i.size[0]/i.size[1])*183*scale)), Image.LANCZOS)
                    
                    i.paste(image_watermark, (i.size[0]-image_watermark.size[0]-50, i.size[1]-image_watermark.size[1]-50), image_watermark)
                
                    i.save('static/img/posts/' + str(latest_id) + '_large.webp', optimize=True, quality=60)

                    # guwniarzu po to że huj wiem co robi ale nie wiem co to jest, ale działa, ale nie wiem jak to zrobić lepiej, ~github copilot
                    # dobra

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

                    latest_id = get_conn().execute(
                        "SELECT seq FROM sqlite_sequence where name='posts'").fetchone()[0]

                    # pierdole to kurwa caly czas sie zapisuje a kurwa wielkosc tego jebanego filmu to kurwa 0 bajtow mam dosc

                    # content_raw.save('static/img/posts_video/' + str(latest_id) + '.mp4')

                    # # 
                    # # video.save('static/img/posts_video/' + str(latest_id) + '.mp4')
                    
                    # is_video = True

                    # user_id = session['user']['id']
                    # date = datetime.now()

                    # conn = get_conn()
                    # c = conn.cursor()

                    # c.execute("INSERT INTO posts (title, description, img_id, user_id, date, is_video)VALUES (?, ?, ?, ?, ?, ?)",
                    #           (title, description, latest_id, user_id, date, is_video))
                    # conn.commit()

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
            "SELECT users.nick, posts.date, posts.title, posts.img_id, posts.description, posts.id, posts.upvotes,posts.downvotes, posts.views, posts.is_video FROM posts,users WHERE posts.id = ? and posts.user_id = users.id", (post_id,))
        post = c.fetchone()
        c.execute("SELECT users.nick,comments.date,comments.content FROM comments,users WHERE comments.post_id = ? and comments.user_id = users.id ORDER BY comments.date", (post_id,))
        comments = c.fetchall()
        
        c.execute("SELECT downvoted FROM posts_votes WHERE user_id = ? and post_id = ?", (session['user']['id'], post_id))
        voted = c.fetchone()
        if voted is not None:
            voted = voted[0]

        return render_template('post_lookup.html', post=post, comments=comments, voted=voted)

@post_app.route("/upvote/<post_id>")
@post_app.route("/upvote/<post_id>/<int:vote_type>")
def upvote(post_id,vote_type=None):
    with current_app.app_context():
        conn = get_conn()
        c = conn.cursor()

        if vote_type == None:
            c.execute("INSERT INTO posts_votes (user_id, post_id, downvoted) VALUES (?, ?, ?)", (session['user']['id'], post_id, 0))
            c.execute("UPDATE posts SET upvotes = upvotes + 1 WHERE id = ?", (post_id,))
            conn.commit()
        elif vote_type == 0:
            c.execute("UPDATE posts SET upvotes = upvotes - 1 WHERE id = ?", (post_id,))
            c.execute("DELETE FROM posts_votes WHERE user_id = ? and post_id = ?", (session['user']['id'], post_id))
            conn.commit()
        elif vote_type == 1:
            c.execute("UPDATE posts SET upvotes = upvotes + 1 WHERE id = ?", (post_id,))
            c.execute("UPDATE posts SET downvotes = downvotes - 1 WHERE id = ?", (post_id,))
            c.execute("UPDATE posts_votes SET downvoted = 0 WHERE user_id = ? and post_id = ?", (session['user']['id'], post_id))
            conn.commit()
        
        return redirect(url_for('post_app.post_lookup', post_id=post_id))

@post_app.route("/downvote/<post_id>")
@post_app.route("/downvote/<post_id>/<int:vote_type>")
def downvote(post_id,vote_type=None):
    with current_app.app_context():
        conn = get_conn()
        c = conn.cursor()


        print(vote_type,vote_type==False)
        if vote_type == None:
            c.execute("INSERT INTO posts_votes (user_id, post_id, downvoted) VALUES (?, ?, ?)", (session['user']['id'], post_id, 1))
            c.execute("UPDATE posts SET downvotes = downvotes + 1 WHERE id = ?", (post_id,))
            conn.commit()
        elif vote_type == 0:
            c.execute("UPDATE posts SET downvotes = downvotes + 1 WHERE id = ?", (post_id,))
            c.execute("UPDATE posts SET upvotes = upvotes - 1 WHERE id = ?", (post_id,))
            c.execute("UPDATE posts_votes SET downvoted = 1 WHERE user_id = ? and post_id = ?", (session['user']['id'], post_id))
            conn.commit()
        elif vote_type == 1:
            c.execute("UPDATE posts SET downvotes = downvotes - 1 WHERE id = ?", (post_id,))
            c.execute("DELETE FROM posts_votes WHERE user_id = ? and post_id = ?", (session['user']['id'], post_id))
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

