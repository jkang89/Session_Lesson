import sqlite3

CONN = sqlite3.connect("thewall.db")
DB = CONN.cursor()

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

def authenticate(username, password):
    query = """SELECT password FROM Users WHERE username = ?"""
    DB.execute(query, (password,))
    password = DB.fetchone()
    
    if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
        return ADMIN_USER
    else:
        return None