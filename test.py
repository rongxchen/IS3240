# import sqlite3
# from general_config import db_path
#
# if __name__ == '__main__':
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         cursor.execute("create table users (id integer primary_key auto_increment, "
#                        "username text unique not null, user_id text unique not null,"
#                        "password text not null)").fetchall()
