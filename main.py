# co tu to robi kurwa!?!?!?!??! xddddddddddddddddddddddddddddddddddddddddddddddddddd
from concurrent.futures import thread
from urllib import response
from flask import Flask, make_response, render_template
from modules.utils import config, get_conn

app = config(Flask(__name__))

@app.before_request
def before_request_func():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT posts.id ,posts.img_id FROM posts ORDER BY RANDOM() LIMIT 1")
    post = c.fetchone()
    app.jinja_env.globals.update(post=post)
    
@app.route('/')
def index():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT posts.id, users.nick, posts.date, posts.img_id  FROM posts,users where posts.user_id = users.id ORDER BY posts.id DESC LIMIT 10")
    posts = c.fetchall()
    
    response = make_response(render_template('index.html', posts=posts))
    return response

# +48 69 69 69 69 call me later <3 :3

if __name__ == '__main__':
    app.run(debug=True)
# smierc ma haslo sex123 nie arek123

# lihrjpnoszghyqjk
