from fastapi import APIRouter
from schemas.users import UesrInfoResponse, UserAuthResponse, UserRequest
from crud import users
from fastapi import HTTPException

from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/register")
async def register(user_data: UserRequest):
    # 驗證用戶是否存在 -> 創建用戶 -> 生成Token -> 返回響應結果
    existing_user = await users.get_user_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户已存在")
    user = await users.create_user(user_data)
    token = await users.create_token(user.id)
    # return {
    #     "code": 200,
    #     "message": "register success",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }
    # model_validate 把数据库ORM对象自动转换成Pydantic模型
    response_data = UserAuthResponse(token=token, user_info=UesrInfoResponse.model_validate(user))
    return success_response(message="register success", data=response_data)

@router.post("/login")
async def login(user_data: UserRequest):
    # 判断用户是否存在 -> 创建Token -> 返回user
    user = await users.login_in(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="错误")
    token = await users.create_token(user_id = user.id)
    response_data = UserAuthResponse(token=token, user_info=UesrInfoResponse.model_validate(user))
    return success_response(message="login success", data = response_data)
