from urllib import response # co tu to robi kurwa!?!?!?!??! xddddddddddddddddddddddddddddddddddddddddddddddddddd
from concurrent.futures import thread
from flask import Flask, current_app, render_template, request
from modules.utils import config, get_conn

app = config(Flask(__name__))

@app.before_request
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
    
@app.route('/')
def index():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT posts.id, users.nick, posts.date, posts.img_id, posts.title  FROM posts,users where posts.user_id = users.id ORDER BY posts.id DESC LIMIT 10")
    posts = c.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/search', methods=['POST'])
def search():
    conn = get_conn()
    c = conn.cursor()
    q = request.form['query']
    c.execute("SELECT posts.id, users.nick, posts.date, posts.img_id, posts.title  FROM posts,users where posts.user_id = users.id and posts.title like ? ORDER BY posts.id DESC LIMIT 10", ('%' + q + '%',))
    posts = c.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

# +48 69 69 69 69 call me later <3 :3

if __name__ == '__main__':
    app.run(debug=True)
# smierc ma haslo sex123 nie arek123

# lihrjpnoszghyqjk
