from models.news import news_category, news
from tortoise.expressions import F

async def get_categories(skip: int = 0, limit: int=100):
    categories = await news_category.all().offset(skip).limit(limit)

    return categories

async def get_news_list(category_id:int, offset:int=0, limit:int = 10):
    # 获取 指定分类下 所有新闻
    news_list = await news.filter(category_id=category_id).offset(offset).limit(limit)

    return news_list

async def get_news_count(category_id:int):
    # 获取 指定分类下 所有新闻的数量
    count = await news.filter(category_id=category_id).count()
    return count

async def get_news_detail(news_id:int):
    news_detail = await news.get_or_none(id=news_id)
    return news_detail

async def increase_news_views(news_id:int):
    # 使用 F 表达式， 直接在数据库层面上直接执行 UPDATE news SET views = views + 1
    # 原子操作，完全并发安全
    news_detail = await news.get_or_none(id=news_id)
    if not news_detail:
        return None

    # 数据库 原子 自增 +1
    count = await news.filter(id=news_id).update(views=F("views")+1) # 返回命中行数
    # 确认修改是否命中
    return True if count > 0 else False

async def get_related_news(news_id:int, category_id:int, limit:int = 5):
    news_list = await news.filter(category_id=category_id).exclude(id=news_id).order_by(
        "-views", "-publish_time"
    ).limit(limit)
    # 列表推导式
    return [{
        "id": news.id,
        "title": news.title,
        "content":news.content,
        "image": news.image,
        "author":news.author,
    } for news in news_list]
