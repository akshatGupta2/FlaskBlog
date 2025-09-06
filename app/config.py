from os import getenv

class Config:
    SECRET_KEY = getenv("SECRET")
    SQLALCHEMY_DATABASE_URI = getenv("SQL_URI")

    # or "sqlite:///C:\\Users\\aksha\\Desktop\\Flask_Tutorial\\flashy_blogs.db"
