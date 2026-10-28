from tortoise import fields, models
from tortoise.indexes import Index

class Base(models.Model):
    # 创建时间
    created_at = fields.DateTimeField(
        auto_now_add=True, # 创建时自动保存时间，后续修改时间不自动更新
        description="创建时间"
    )

    # 更新时间
    updated_at = fields.DateTimeField(
        auto_now=True, # 每次ORM保存更新，自动更新时间
        description="更新时间"
    )

    class Meta:
        abstract = True # 抽象基类

class news_category(Base):
    id:  int = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=False, unique=True, description="学生姓名")
    sort_order = fields.IntField(null=False, default=0, description="排序")

    def __str__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"

    class Meta:
        table = "news_category"

class news(Base):
    id:int = fields.IntField(pk=True, description="新闻ID")
    title = fields.CharField(max_length=255, null= False, description="新闻标题")
    description = fields.CharField(max_length=500, description="新闻简介")
    content = fields.TextField(null=False, description="新闻内容")
    image = fields.CharField(max_length=255, description="封面图片URL")
    author = fields.CharField(max_length=50, description="作者")
    category = fields.ForeignKeyField("models.news_category", related_name="category", null=False)
    # ForeignKeyField 会自动加 _id
    views = fields.IntField(default=0, null=False, description="浏览量")
    publish_time = fields.DateField(auto_now_add=True, description="发布时间")

    def __str__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"

    class Meta:
        table = "news"
        indexes = [
            Index(
                fields=["category_id"],
                name="fk_news_category_idx",
            ),
            Index(
                fields=["publish_time"],
                name="idx_publish_time"
            ),
        ]
