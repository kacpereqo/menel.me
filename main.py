from email.policy import default
from flask import Flask, current_app, flash, redirect, render_template, request, session
from modules.utils import config, get_conn
from math import ceil

app = config(Flask(__name__))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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

@app.route('/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/<int:page>', methods=['GET', 'POST'])
def index(page, **kwargs):

    valid_requests = ("hot", "views","upvotes","id","1","7","30","999"," ","DESC") 

    if page < 1:
        page = 1
    if request.method == 'POST':
        sort_by = request.form['sort_by']
        time = request.form['time']
        order = request.form['order']
    elif request.args:
        sort_by = request.args.get('sort_by')
        time = request.args.get('time')
        order = request.args.get('order')
    else:
        sort_by = "id"
        time = "999"
        order = "DESC"

    if sort_by not in valid_requests or time not in valid_requests or order not in valid_requests:
        flash("sex")
        return render_template('kontakt.html')

    conn = get_conn()
    c = conn.cursor()
    c.execute(f"SELECT posts.id, users.nick, posts.date, posts.img_id, posts.title, posts.views, posts.upvotes, posts.downvotes, posts.category FROM posts,users where (posts.user_id = users.id and posts.date > DATE('now', '-{time} day'))   ORDER BY posts.{sort_by} {order} LIMIT 7 OFFSET {(page-1)*7}")
    posts = c.fetchall()
    c.execute(f"SELECT COUNT(*) FROM posts  where date > DATE('now', '-{time} day')")
    page_count = ceil(c.fetchone()[0]/7)
    
    return render_template('index.html', posts=posts, page=page,page_count = page_count, sort_by=sort_by, time=time, order=order)

@app.route('/search', methods=['POST'])
def search():
    conn = get_conn()
    c = conn.cursor()
    q = request.form['query']
    c.execute("SELECT posts.id, users.nick, posts.date, posts.img_id, posts.title, posts.views, posts.upvotes, posts.downvotes, posts.category  FROM posts,users where posts.user_id = users.id and posts.title like ? ORDER BY posts.id DESC LIMIT 10", ('%' + q + '%',))
    posts = c.fetchall()
    
    c.execute("SELECT COUNT(*) FROM posts WHERE title like ?", ('%' + q + '%',))
    page_count = ceil(c.fetchone()[0]/7)
    return render_template('index.html', posts=posts, page=1, page_count=page_count)

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')
    # ale zes dojebal tego kontakta B)

# +48 69 69 69 69 call me later <3 :3

if __name__ == '__main__':
    app.run(debug=True)
# smierc ma haslo sex123 nie arek123

# lihrjpnoszghyqjk
