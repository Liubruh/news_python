TORTOISE_ORM = {
    "connections": {
        "default": "postgresql://neondb_owner:npg_aZ8uh2wEKVvQ@ep-twilight-cherry-aze4s6m9-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb"
    },
    "apps": {
        "models": {
            "models": ["models.news", "models.user"],  # 注意：必须加上 "aerich.models"
            "default_connection": "default",
        }
    },
}
