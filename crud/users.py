from schemas import users
from models import users
def get_user_username(user_data: users.UserRequest):
    user = await users.User.get_or_none(username=user_data.username)
    return user

def create_user(user_data: users.UserRequest):
    # 加密
    user = await users.User.create()
