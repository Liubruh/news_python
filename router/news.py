from fastapi import APIRouter, HTTPException, Query
from crud import news
router = APIRouter(prefix="/api/news", tags=['news'])

# 添加路由 -> 定义模型类 -> 封装CRUD方法 -> 路由处理函数调用方法

@router.get("/categories")
async def get_categoroies(skip: int = 0, limit: int = 100):
    categories = await news.get_categories(skip, limit)

    return {
        "code": 200,
        "message":"获取新闻分类",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
    category_id: int =  Query(..., alias="categoryId"),
    page:int = 1,
    page_size: int = Query(10, alias="pageSize", le=100),
):
    # 处理分页规则 -> 查询新闻列表 -> 计算总量 -> 计算是否还有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(category_id, offset, page_size)
    total_count = await news.get_news_count(category_id)
    has_more = (offset + len(news_list)) < total_count
    return {
        "code": 200,
        "message": "success",
        "data":{
            "list": news_list,
            "total": total_count,
            "hasMore": has_more
        }
    }

@router.get("/detail")
async def get_news_detail(news_id:int = Query(..., alias="id")):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    news_detail = await news.get_news_detail(news_id)
    if not news_detail:
        raise HTTPException(
            status_code=404,
            detail="Not Found！"
        )
    right = await news.increase_news_views(news_id)
    if not right:
        raise HTTPException(
            status_code=404,
            detail="Not Found！"
        )
    related_list = await news.get_related_news(news_id, news_detail.category_id)
    return {
        "code": 200,
        "message": "success",
        "data":{
            "id": news_detail.id,
            "title": news_detail.title,
            "content":news_detail.content,
            "image": news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":related_list
        }
    }
