import sqlite3

CONN = sqlite3.connect("thewall.db")
DB = CONN.cursor()

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

def authenticate(username, password):


    if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
        return ADMIN_USER
    else:
        return None

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