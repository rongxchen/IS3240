import sqlite3

db_name = "./sqlite3.db"

def login(username, password):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        user = cursor.execute("select password from users where username = ?", [username]).fetchall()
    return len(user) > 0 and user[0][0] == password

def register(username, password):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        users = cursor.execute("select 1 from users where username = ?", [username]).fetchall()
        if len(users) == 0:
            cursor.execute("insert into users (username, password) values (?, ?)", (username, password))
            conn.commit()
            cursor.close()

def change_password(username, new_password):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("update users set password = ? where username = ?", (new_password, username))
        conn.commit()
        cursor.close()

def delete_user(username):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("delete from users where username = ?", [username])
        conn.commit()
        cursor.close()
