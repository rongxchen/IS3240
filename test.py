# import sqlite3
# from general_config import db_path
#
# if __name__ == '__main__':
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         cursor.execute("create table users (id integer primary_key auto_increment, "
#                        "username text unique not null, user_id text unique not null,"
#                        "password text not null)").fetchall()

from utils.jwt_util import verify_token
if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlci1mM2FlYmE3My0yZWZkLTQzYWYtYTI5MS1mMmJiMDNhYWI3YTgiLCJleHAiOjE2OTYwODQ0Njc5Mjd9.NqxP3dqQhaFoCFLjndqj8C8uLcOpY3YGED9eooQql6Q"
    verify_token(token)