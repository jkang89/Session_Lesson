import sqlite3

DB = None
CONN = None

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

def connect_to_db(): 
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def authenticate(username, password):
    query_username = """SELECT username from users WHERE password = ?"""
    query_password = """SELECT password from users WHERE username = ?"""
    DB.execute(query_username, (password,))
    DB.execute(query_password, (username,))
    username = DB.fetchone()
    password = DB.fetchone()

    print username
    print password

    # if username == query_username and hash(password) == hash(query_password):
    #     return username
    # else:
    #     return None

def get_user_by_name(username):
    query = """SELECT * FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    return row

def get_wallposts_by_user(user_id):
    query = """SELECT * FROM wall_posts WHERE user_id = ?"""
    DB.execute(query, (user_id,))
    rows = DB.fetchall()
    return rows

def add_new_post(user_id, owner_id, author_id, created_at, content):
    query = """INSERT into wall_posts VALUES (?,?,?,?,?)"""
    DB.execute(query, (user_id, owner_id, author_id, created_at, content))
    CONN.commit()

def new_user_id():
    query_last_user_id = """SELECT user_id FROM users"""
    DB.execute(query_last_user_id,)
    user_ids = DB.fetchall()
    user_id = user_ids[-1][0] + 1
    return user_id

def add_new_user(user_id, username, password):

    query = """INSERT into users VALUES (?,?,?)"""
    DB.execute(query, (user_id, username, password))
    CONN.commit()

connect_to_db()
authenticate("ferret_boy", "ferret")