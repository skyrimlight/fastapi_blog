from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
# from Blog.models import Blog_User as User
from Blog.until import setting as settings
from Blog.until.get_md5 import get_md5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="././auth/blog/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码 vs hash密码
    :param plain_password: 明文密码
    :param hashed_password: hash密码
    :return:
    """
    plain_password = get_md5(plain_password)
    if plain_password == hashed_password:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户名或密码错误')
    # return plain_password == hashed_password


def get_password_hash(password: str) -> str:
    """
    加密明文
    :param password: 明文密码
    :return:
    """
    return get_md5(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    生成token
    :param data: 字典
    :param expires_delta: 有效时间
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    # to_encode.update({"user_id": expire})
    # print(data)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return payload
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     """
#     # oauth2_scheme -> 从请求头中取到 Authorization 的value
#     解析token 获取当前用户对象
#     :param token: 登录之后获取到的token
#     :return: 当前用户对象
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
#         username: str = payload.get("sub", None)
#     except JWTError:
#         raise credentials_exception
#
#     # username: str = payload.get("sub", None)
#     print("11111111111111111111111111111" + username)
#     if username is None:
#         raise credentials_exception
#
#     # user = await User.get(username=username)
#     # redis
#     # if await request.app.state.redis.get(user.username) is None:
#     #     raise HTTPException(detail='redis 数据失效', status_code=status.HTTP_408_REQUEST_TIMEOUT)
#     # if user is None:
#     #     raise credentials_exception
#     return username
