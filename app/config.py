from os import getenv
class Config:
    SECRET_KEY = 'caa4666641a41891d231c5dc39174e24'
    SQLALCHEMY_DATABASE_URI = getenv("SQL_URI") or "sqlite:///C:\\Users\\aksha\\Desktop\\Flask_Tutorial\\flashy_blogs.db"