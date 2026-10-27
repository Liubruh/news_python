from datetime import datetime

from tortoise import fields
from tortoise.models import Model
from tortoise.indexes import Index
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

class User(Model):
    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=50, unique=True, null=False, description="用户名")
    password = fields.CharField(max_length=255, null=False, description="密码(加密)")
    nickname = fields.CharField(max_length=50, null=True, description="昵称")
    avatar = fields.CharField(max_length=255, default='https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg')
    gender = fields.CharEnumField(
        Gender,
        default=Gender.UNKNOWN,
        null=True,
        description="性別"
    )
    bio = fields.CharField(max_length=500, default="lazy", description="個人簡介")
    phone = fields.CharField(max_length=20, unique=True, description="手機號")
    created_at = fields.DateTimeField(auto_now_add=True, description="創建時間", default=datetime.now())
    updated_at = fields.DateTimeField(auto_now=True, default=datetime.now(), description="修改時間")

    def __str__(self):
        return f"<User(id={self.id},username='{self.username}',nickname='{self.nickname}'>"

    class Meta:
        table="user"
        indexes = [
            Index(
                fields=['username'],
                name="username_UNIQUE",
            ),
            Index(
                fields=['phone'],
                name="phone_UNIQUE",
            )
        ]

class UserToken(Model):
    id = fields.IntField(pk=True, description="令牌ID")
    user = fields.ForeignKeyField("models.User", null=False, description="用戶ID")
    token = fields.CharField(max_length=255, unique=True, null=False, description="令牌值")
    # DateTimeFields -> 日期+時間; DataFields -> 時間;
    expires_at = fields.DateTimeField(null=False, description="過期時間")
    created_at = fields.DateTimeField(default=datetime.now(), description="創建時間")

    def __str__(self):
        return f"<UserToken(id={self.id}, user_id={self.user.id},token='{self.token}'"

    class Meta:
        table="user_token"
        indexes = [
            Index(
                fields=['token'],
                name = "token_UNIQUE"
            ),
            Index(
                fields=['user_id'],
                name="fk_user_token_idx"
            )
        ]
