from time import time
from random import random
from sqlalchemy.orm import Session
import uvicorn
from fastapi import FastAPI, Request, responses, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import time

from Blog.admin import admin
from Blog.blog import blog
from Blog.until.get_md5 import get_user_md5
from Blog import models, crud
from Blog.database import engine, Base, SessionLocal
from Blog.auth import auth
import redis

app = FastAPI(
    title='Blog后端，基于FastAPI',
    description='Blog项目后续，基于FastAPI完成API接口文档',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs')

# 进行挂载
# register_redis(app)

app.include_router(auth, prefix='/auth', tags=["用户"])
app.include_router(blog, prefix='/blog', tags=["博客"])
app.include_router(admin, prefix='/admin', tags=["管理员"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/blog/login')

# 挂载静态文件,mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/static', app=StaticFiles(directory='Blog/static'), name='static')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.middleware('http')
# async def login_check(request: Request, call_next, token: str = Depends(oauth2_scheme)):  # call_next将接收request请求做为参数
#     # if request.headers.get('X-Process-User'):
#     #     user_level = redis.Redis.get(request.headers['X-Process-User'])
#     # if user_level > 5:
#     print(request.path_params)
#     # usernmae = redis.Redis.get()
#     # start_time = time.time()
#     # redis.Redis.delete('xqwp')
#     # user = redis.Redis.get()
#     response = await call_next(request)
#     # process_time = time.time() - start_time
#     # response.headers['X-Process-User'] = get_user_md5()  # 添加自定义的以“X-”开头的请求头
#     # print(process_time)
#
#     return response
#     # return response
#
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://127.0.0.1",
#         "http://127.0.0.1:8080"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# app.include_router(app03, prefix='/chapter03', tags=["第三章"])

@app.get('/')
async def index(page: int = 1, db: Session = Depends(get_db)):
    post = crud.get_index_post(db=db, skip=page, limit=3)
    tags = crud.get_index_tag(db=db, limit=6)
    img_banner = crud.get_index_img(db=db, limit=3)
    category = crud.get_index_catagory(db=db)
    imgs = [
        'https://th.bing.com/th/id/R.d8dfd08893b58d08d74b38ad8870a48d?rik=FOH776EhG01I%2bA&riu=http%3a%2f%2fstatic.cntonan.com%2fuploadfile%2f2020%2f0318%2f20200318122901txdvkwgvpsw.jpg&ehk=2OKIaIz3xTccGgjf5DFKNDfJLcPfvXjuF%2bJbC6GJk6w%3d&risl=&pid=ImgRaw&r=0',
        'https://th.bing.com/th/id/R.466bb61cd7cf4e8b7d9cdf645add1d6e?rik=YRZKRLNWLutoZA&riu=http%3a%2f%2f222.186.12.239%3a10010%2fwmxs_161205%2f002.jpg&ehk=WEy01YhyfNzzQNe1oIqxwgbTnzY7dMfmZZHkqpZB5WI%3d&risl=&pid=ImgRaw&r=0',
        'https://th.bing.com/th/id/R.987f582c510be58755c4933cda68d525?rik=C0D21hJDYvXosw&riu=http%3a%2f%2fimg.pconline.com.cn%2fimages%2fupload%2fupc%2ftx%2fwallpaper%2f1305%2f16%2fc4%2f20990657_1368686545122.jpg&ehk=netN2qzcCVS4ALUQfDOwxAwFcy41oxC%2b0xTFvOYy5ds%3d&risl=&pid=ImgRaw&r=0']
    img_dict = {}
    for index, url in enumerate(imgs):
        img_dict[index] = url
    content = {
        'category': category,
        "post": post,
        "tags": tags,
        "img_banner": img_banner,
        "img_dict": img_dict
    }
    return content


if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, workers=4)
