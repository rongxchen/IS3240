from models.model import User, session
from models.util import generate_id
from utils.cipher import md5_encrypt

def login(username, password):
    users = session.query(User).all()
    user = session.query(User).filter_by(username=username).first()
    _password = md5_encrypt(password)
    if not user or user.password != _password:
        return False, "wrong username or password", None
    return True, "authorized", user.user_id

def register(username, password):
    find = session.query(User).filter_by(username=username).first()
    if find:
        return False, "username already registered"
    user_id = generate_id("user")
    user = User(username, user_id, md5_encrypt(password))
    session.add(user)
    session.commit()
    return True, "registered"

def change_password(user_id, new_password):
    find = session.query(User).filter_by(user_id=user_id).first()
    if not find:
        return False, "no such user"
    _password = md5_encrypt(new_password)
    if find.password == _password:
        return False, "new password cannot be the same as the old one"
    find.password = _password
    session.add(find)
    session.commit()
    return True, "password changed"

def delete_account(user_id):
    find = session.query(User).filter_by(user_id=user_id).first()
    if not find:
        return False, "no such user"
    session.delete(find)
    session.commit()
    return True, "account deleted"
