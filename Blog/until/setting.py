import secrets

from Blog.database import SessionLocal

BASE_DIR = r'C:\Users\10708\Desktop\认识python\web项目\fastApi_Blog\Blog\static\img'
ALGORITHM: str = "HS256"  # 加密算法
SECRET_KEY: str = secrets.token_urlsafe(32)  # 随机生成的base64位字符串
# SECRET_KEY: str = 't4bbDwxtMzj9efw+iiKqlZDpUzUBbG9emWyNys0DTdQ='  # 随机生成的base64位字符串
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # token的时效 3 天 = 60 * 24 * 3


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
