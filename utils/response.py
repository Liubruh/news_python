# 封装通用成功相应格式

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message:str ="success", data: any= None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    return JSONResponse(
        content=jsonable_encoder(content)
    )