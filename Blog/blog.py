from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Blog import crud, schemas, models
from Blog.core import security
from Blog.until.setting import get_db

blog = APIRouter(prefix='/blog')
"""文章系统"""


# @blog.get('/post_detail', response_model=schemas.PostDetails)
@blog.get('/post_detail/{cate_id}/{post_id}')
async def post_detail(post_id: int, page: int = 0, db: Session = Depends(get_db),
                      user_obj: models.Blog_User = Depends(security.get_current_user)):
    print(post_id)
    return crud.get_post_detail(db=db, post_id=post_id, page=page)


# 获取文章内容评论和首页最新文章、文章标签、归档选项
@blog.get('/post_detail/{cate_id}')
async def post_detail(cate_id: int, page: int = 0, db: Session = Depends(get_db),
                      user_obj: models.Blog_User = Depends(security.get_current_user)):
    return crud.get_post_detail(db=db, cate_id=cate_id, page=page)


# 根据标签获取文章
@blog.get('/tag/{tag_id}')
async def tag_detail(tag_id: int, page: int = 0, db: Session = Depends(get_db),
                     user_obj: models.Blog_User = Depends(security.get_current_user)):
    return crud.get_post_by_tag(db=db, tag_id=tag_id, page=page)


# 根据日期归档检索文章
@blog.get('/category/{date}')
async def tag_detail(date: str, page: int = 0, db: Session = Depends(get_db),
                     user_obj: models.Blog_User = Depends(security.get_current_user)):
    return crud.archive(db=db, date=date, page=page)


# 搜索文章
@blog.get('/search_posts_by_title')
async def search_posts(q: str, page: int = 0, db: Session = Depends(get_db),
                       user_obj: models.Blog_User = Depends(security.get_current_user)):
    return crud.search_posts_by_title(db=db, q=q, page=page)
