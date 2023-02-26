from typing import Optional, List, Any

from fastapi import APIRouter, Request, Depends, HTTPException, status, UploadFile, File
from Blog.core import verify_password, create_access_token, deps, security

from sqlalchemy.orm import Session

from Blog import schemas, models
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from Blog.crud import modify_user_avatar
from Blog.schemas import ResponseToken, Response400
from Blog.until.file_upload import upload_file_one
from Blog.database import engine, Base, SessionLocal, redis
from Blog import crud
from Blog.until.setting import get_db

auth = APIRouter(prefix='/blog')

#
# @auth.post('/login')
# async def login(username: str, password: str, db: SessionLocal = Depends(get_db)):
#     password_md5 = get_md5(password)
#     user_info = crud.check_user(db=db, username=username, password=password_md5)
#     if user_info:
#         redis.set(name=user_info.username, value=, ex=)
#         return {'msg': '登陆成功'}
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='用户名或密码错误')

# SECRET_KEY = "ed970259a19edfedf1010199c7002d183bd15bcaec612481b29bac1cb83d8137"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# def create_jwt_token(data: dict, expire_delta: Optional[timedelta] = None):
#     # 如果传入了过期时间, 那么就是用该时间, 否则使用默认的时间
#     expire = datetime.utcnow() + expire_delta if expire_delta else datetime.utcnow() + timedelta(
#         minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     # 需要加密的数据data必须为一个字典类型, 在数据中添加过期时间键值对, 键exp的名称是固定写法
#     data.update({'exp': expire})
#     # 进行jwt加密
#     token = jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)
#     return token

# temp注释
# @auth.post('/login', response_model=schemas.User_info)
# async def login(username: str, password: str, request: Request, db: SessionLocal = Depends(get_db)):
#     # user_name = form_data.username
#     # password = form_data.password
#     request.headers
#     password_md5 = get_md5(password)
#     user_info = crud.check_user(db=db, username=username, password=password_md5)
#     if not user_info:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='用户名或密码错误')
#     redis.set(name=user_info.username, value=1, ex=604800)
#     return user_info

"""用户系统"""


# return {"access_token": get_user_md5(user_name), "token_type": "bearer"}
@auth.post("/login", summary="登录")
async def user_login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.Blog_User).filter(models.Blog_User.username == form_data.username).first()
    if user:
        if verify_password(form_data.password, user.password):
            if user.is_super_user:
                token = create_access_token({"sub": user.username, 'id': user.id, 'level': 2})
            else:
                token = create_access_token({"sub": user.username, 'id': user.id, 'level': 1})
        redis.set(name=user.username, value=token, ex=604800)
        return ResponseToken(data={"token": f"bearer {token}"}, access_token=token)
    return Response400(msg="请求失败.")


@auth.post('/register', response_model=schemas.User, summary='注册')
async def register(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user_info = crud.get_user_by_username(db, username=user.username)
    if user_info:
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail='用户已经存在')
    return crud.user_register(db, user)


@auth.get('/logout', summary='注销')
async def register(db: Session = Depends(get_db),
                   user_obj: models.Blog_User = Depends(security.get_current_user)):
    user_info = crud.get_user_by_username(db, username=user_obj['sub'])
    redis.delete(user_info.username)
    return {'msg': '注销成功'}


# 获取用户评论

@auth.get('/user/comments', response_model=List[schemas.get_user_comments])
async def get_user_comments(db: Session = Depends(get_db),
                            user_obj: models.Blog_User = Depends(security.get_current_user)):
    return crud.get_user_comments(db=db, user_id=user_obj['id'])


# 用户删除评论
@auth.delete('/delete/comment')
async def delete_comment(comment_id: int, db: Session = Depends(get_db),
                         user_obj: models.Blog_User = Depends(security.get_current_user)):
    comment_info = crud.get_user_comments_by_comment(db=db, comment_id=comment_id)
    if not comment_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='没有此评论')
    crud.delete_user_comments(db=db, comment_id=comment_id)
    return {"status_code": status.HTTP_200_OK, "msg": "删除成功"}


# 获取用户信息
@auth.get('/user_info', response_model=schemas.User_info)
async def modify_user_info(db: Session = Depends(get_db),
                           user_obj: models.Blog_User = Depends(security.get_current_user)):
    user_info = crud.get_user_by_user_id(db=db, user_id=user_obj['id'])
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='没有此用户')
    return user_info


# 修改用户头像
@auth.patch('/upload_avatar', response_model=schemas.User_info)
async def upload_avatar(db: Session = Depends(get_db), file: UploadFile = File(...),
                        user_obj: models.Blog_User = Depends(security.get_current_user)):
    file_avatar = upload_file_one(file)
    filename = file_avatar['filename']
    user_info = modify_user_avatar(user_id=user_obj['id'], filename=filename, db=db)
    return user_info


# 修改用户信息
@auth.put('/update_user_info', response_model=schemas.User_info)
async def update_user_info(user: schemas.Update_user, db: Session = Depends(get_db),
                           user_obj: models.Blog_User = Depends(security.get_current_user)):
    user_info = crud.modify_user_info(db=db, user=user, username=user_obj['sub'])
    return user_info
