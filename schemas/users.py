from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    """ 用户信息基础数据类型 """
    nickname: Optional[str] = Field(None, max_length=50)
    avatar: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field(None, max_length=10)
    bio: Optional[str] = Field(None, max_length=500)

class UesrInfoResponse(UserInfoBase):
    id: int
    username: str
    
    model_config = ConfigDict(
        from_attributes=True, # 允许从 ORM 对象属性中取值
    )

class UserAuthResponse(BaseModel):
    token: str
    user_info: UesrInfoResponse = Field(..., alias="userInfo") # 取别名

    model_config = ConfigDict(
        populate_by_name=True, # alias 和字段名兼容
        from_attributes=True, # 允许从 ORM 对象属性中取值
    )