# sqlite 3 database setup
import sqlite3
conn = sqlite3.connect('data/db/database.sqlite')
c = conn.cursor()

# c.execute("""CREATE TABLE users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nick text,
#     password text,
#     email text
# )""")

# create table posts id unique content img description text user_id integer upvotes int downvotes int
# c.execute("""CREATE TABLE posts (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title text NOT NULL,
#     description text NOT NULL,
#     content BLOB NOT NULL,
#     user_id integer NOT NULL,
#     upvotes int DEFAULT 0,
#     downvotes int DEFAULT 0
# )""")

# add date colum to posts
# c.execute("""ALTER TABLE posts ADD COLUMN date text""")

# delete all records from posts
# c.execute("""DELETE FROM posts where id = 13 """)
# conn.commit()

# c.execute("SELECT * FROM 'posts','users' WHERE posts.user_id = users.id ORDER BY posts.id DESC LIMIT 10")
# posts = c.fetchall()
# print(posts[0][8])

# create comments table 
# c.execute("""CREATE TABLE comments (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     content text NOT NULL,
#     date text NOT NULL,
#     user_id integer NOT NULL,
#     post_id integer NOT NULL
# )""")

# add active status to users
# c.execute("""ALTER TABLE users ADD COLUMN activedwa boolean""")

# add status to user (ex: banned)
# c.execute("""ALTER TABLE users ADD COLUMN reason text""")

# add token to user (ex: activation token)
# c.execute("""ALTER TABLE users ADD COLUMN token text""")

# c.execute("""CREATE TABLE users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nick text,
#     password text,
#     email text,
#     active boolean,
#     reason text,
#     token text
# )""")

# clear table users

# create table upvoted user_id integer post_id integer comment_id
# c.execute("""CREATE TABLE voted (
#     user_id integer NOT NULL,
#     post_id integer,
#     comment_id integer)""")
# chnage posts column content to img_id
c.execute("""ALTER TABLE posts
RENAME COLUMN content TO img_id""")

# c.execute("DELETE FROM posts")
# conn.commit()