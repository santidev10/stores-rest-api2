from werkzeug.security import safe_str_cmp
from models.user import UserModel     # import UserModel class from models/user.py (now 'models' is a package because it contains" __init__.py")

def authenticate(username, password):
    user = UserModel.find_by_username(username)                # it returns a user entity (user class)(internal entity)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
