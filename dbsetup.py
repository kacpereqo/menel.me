# sqlite 3 database setup
import sqlite3
conn = sqlite3.connect('database.sqlite')
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
# c.execute("""DELETE FROM posts where id = 9 or id = 10""")
# conn.commit()

c.execute("SELECT * FROM 'posts','users' WHERE posts.user_id = users.id ORDER BY posts.id DESC LIMIT 10")
posts = c.fetchall()
print(posts[0][8])