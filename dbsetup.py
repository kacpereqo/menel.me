# sqlite 3 database setup
import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("""CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nick text,
    password text,
    email text
)""")
