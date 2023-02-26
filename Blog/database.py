from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from redis import StrictRedis

HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'skyrimlight'
PASSWORD = 'skyrimlight'
DATABASE = 'flask'
DB_URL = F'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
SQLALCHEMY_DATABASE_URI = DB_URL
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本的映射类

# Base = declarative_base(, name="Base")
Base = declarative_base()
redis = StrictRedis(host='localhost', port=6379, db=2, encoding='utf-8', decode_responses=True)
