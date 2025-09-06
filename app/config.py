from os import getenv
class Config:
    SECRET_KEY = 'caa4666641a41891d231c5dc39174e24'
    SQLALCHEMY_DATABASE_URI = "postgresql://neondb_owner:npg_SoRf3ms4duVh@ep-solitary-river-a19htapa-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    # or "sqlite:///C:\\Users\\aksha\\Desktop\\Flask_Tutorial\\flashy_blogs.db"