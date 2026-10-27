from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import uvicorn
from router import news,user
from config.database import TORTOISE_ORM

from fastapi.middleware.cors import CORSMiddleware

# API 接口文档 、 数据库模型文档

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"], # 允许的请求方法
    allow_headers=["*"], # 允许的请求头
)

app.include_router(news.router)
app.include_router(user.router)

register_tortoise(
    app,
    config = TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
