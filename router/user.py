from fastapi import APIRouter
from schemas import users

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/register")
async def register(user_data: users.UserRequest):
    # 驗證用戶是否存在 -> 創建用戶 -> 生成Token -> 返回響應結果

    return {
        "code": 200,
        "message": "register success",
        "data": {
            "token": "token",
            "userInfo": {
                "id": 1,
                "username": user_data.username,
                "bio": "1",
                "avatar": "jpg"
            }
        }
    }
