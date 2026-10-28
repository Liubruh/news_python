from schemas.users import UserRequest
from models import users
from utils import security
import uuid 
from datetime import datetime, timedelta

async def get_user_username(username: str):
    user = await users.User.get_or_none(username=username)
    return user

async def create_user(user_data:UserRequest):
    pwd = security.get_hash_password(user_data.password)
    user = await users.User.create(username = user_data.username, password = pwd)
    return user

async def create_token(user_id:int):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)

    user_token = await users.UserToken.get_or_none(user_id=user_id)

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = await users.UserToken.create(user_id=user_id, token=token, expires_at=expires_at)

    return token

async def login_in(username:str, password: str):
    user = await get_user_username(username=username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user
