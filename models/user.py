import sqlite3
from static_variables import db_path
from utils.cipher import md5_encrypt

def login(username, password):
    _password = md5_encrypt(password)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        user = cursor.execute("select password from users where username = ?", [username]).fetchall()
    return len(user) > 0 and user[0][0] == _password

def register(username, password):
    _password = md5_encrypt(password)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        users = cursor.execute("select 1 from users where username = ?", [username]).fetchall()
        if len(users) == 0:
            cursor.execute("insert into users (username, password) values (?, ?)", (username, _password))
            conn.commit()
            cursor.close()
            return True, "register ok"
    return False, "username existed already"

def change_password(username, password, new_password):
    if password == new_password:
        return False, "new password cannot be the same as the old one"
    _password = md5_encrypt(new_password)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("update users set password = ? where username = ?", (_password, username))
        conn.commit()
        cursor.close()
    return True, "password changed"

def delete_user(username):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("delete from users where username = ?", [username])
        conn.commit()
        cursor.close()
