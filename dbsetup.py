# sqlite 3 database setup
import sqlite3
conn = sqlite3.connect('db/database.sqlite')
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
# c.execute("""ALTER TABLE posts
# RENAME COLUMN content TO img_id""")

#add views column to posts
# c.execute("""ALTER TABLE posts
# ADD COLUMN views integer DEFAULT 0""")


# # c.execute("DELETE FROM posts")
# # conn.commit()


# delete column comment_id from voted
# c.execute("""ALTER TABLE voted
# DROP COLUMN comment_id""")
# conn.commit()

# add column upvoted bool
# c.execute("""ALTER TABLE voted
# # ADD COLUMN upvoted boolean NOT NULL""")

# add column upvoted bool
# c.execute("""ALTER TABLE posts_votes
# ADD COLUMN downvoted boolean NOT NULL""")

# c.execute("""ALTER TABLE users ADD COLUMN created date""")
# c.execute("""ALTER TABLE users ADD COLUMN last_login date""")
# add description to users

# c.execute("""ALTER TABLE users ADD COLUMN description text""")
# add location to users
# c.execute("""ALTER TABLE users ADD COLUMN location text""")
# set description where id = 12
# c.execute("""UPDATE users SET description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer aliquam libero lectus, vel auctor dolor imperdiet id. Aliquam elementum cursus purus, ut convallis felis malesuada id. Integer suscipit cursus mi, vel vulputate erat vehicula varius. Mauris et iaculis est. Nam ut ligula ut nunc congue tempor ut nec quam. Morbi facilisis dui vel feugiat feugiat. Sed non nisi vitae quam tincidunt tristique eu at enim. ' WHERE id = 11""")
# c.execute("SELECT *  FROM posts where posts.user_id = ?", (11,))
# print(len(c.fetchall()))
# add to post column category list

# c.execute("""ALTER TABLE posts
# ADD COLUMN category text""")
# add table categories id uniqe, name category 
# c.execute("""CREATE TABLE categories (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name text
# )""")
# add category 

# add table post_categories id unique post_id integer category_id integer
# c.execute("""CREATE TABLE post_categories (
#         post_id integer NOT NULL,
#     category_id integer NOT NULL
# )""")

# clear table posts
# c.execute("DELETE FROM posts")

# add column f to posts
# c.execute("""ALTER TABLE posts
# ADD COLUMN file_name text""")

# add column f to posts
c.execute("""ALTER TABLE posts
ADD COLUMN file_name text""")
conn.commit()