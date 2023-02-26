from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from Blog import crud, schemas, models
from Blog.core import security
from Blog.until.setting import get_db

admin = APIRouter(prefix='/admin')


# 管理员首页数据
@admin.get('/index', summary='管理员首页')
def admin_index(db: Session = Depends(get_db), user_obj: models.Blog_User = Depends(security.get_current_user)):
    print(user_obj['level'])
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_index(db=db)


# 管理员分类管理
# 查询分类
@admin.get('/category', response_model=List[schemas.Admin_Category_Get], summary='查询分类')
def admin_category_get(page: int = 0, db: Session = Depends(get_db),
                       user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_category_get(db=db, page=page)


# 增加分类
@admin.post('/category/add', response_model=schemas.Admin_Category_Add, summary='增加分类')
def admin_category_add(category: schemas.Admin_Category_Add, db: Session = Depends(get_db),
                       user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_category_add(db=db, category=category)


# 根据分类id查询分类
@admin.get('/category/edit/{category_id}', response_model=schemas.Admin_Category_Get, summary='查询分类')
def admin_category_by_id(category_id: int, db: Session = Depends(get_db),
                         user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_category_by_id(db=db, category_id=category_id)


# 修改分类
@admin.put('/category/edit/{category_id}', response_model=schemas.Admin_Category_Add, summary='修改分类')
def admin_category_edit(category_id: int, category: schemas.Admin_Category_Add, db: Session = Depends(get_db),
                        user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_category_edit(db=db, category=category, category_id=category_id)


# 删除分类
@admin.delete('/category/delete/{category_id}', summary='删除分类')
def admin_category_edit(category_id: int, db: Session = Depends(get_db),
                        user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    crud.admin_category_delete(db=db, category_id=category_id)
    return {'msg': '分类删除成功'}


# 管理员文章管理
# 查询文章
@admin.get('/article', response_model=List[schemas.Admin_Article_Get], summary='查询文章')
def admin_article_get(page: int = 0, db: Session = Depends(get_db),
                      user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_article_get(db=db, page=page)


class Category_Post(str, Enum):
    flask1 = 'flask'
    fastapi2 = 'fastapi'
    django3 = 'django'


# 增加文章
@admin.post('/article/add', response_model=schemas.Admin_Article_Add, summary='增加文章')
def admin_article_add(article: schemas.Admin_Article_Add, category_id: Category_Post, db: Session = Depends(get_db),
                      user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_article_add(db=db, article=article, category_id=category_id)


# 根据文章id查询文章
@admin.get('/article/edit/{article_id}', response_model=schemas.Admin_Article_Get, summary='查询文章')
def admin_article_by_id(article_id: int, db: Session = Depends(get_db),
                        user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_article_by_id(db=db, article_id=article_id)


# 修改文章
@admin.put('/article/edit/{article_id}', response_model=schemas.Admin_Article_Add, summary='修改文章')
def admin_article_edit(article_id: int, article: schemas.Admin_Article_Add, db: Session = Depends(get_db),
                       user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_article_edit(db=db, article=article, article_id=article_id)


# 删除文章
@admin.delete('/article/delete/{article_id}', summary='删除文章')
def admin_article_edit(article_id: int, db: Session = Depends(get_db),
                       user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    crud.admin_article_delete(db=db, article_id=article_id)
    return {'msg': '文章删除成功'}


# 管理员文章标签
# 查询文章标签
@admin.get('/tag', response_model=List[schemas.Admin_Tag_Get], summary='查询文章标签')
def admin_tag_get(page: int = 0, db: Session = Depends(get_db),
                  user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_tag_get(db=db, page=page)


# 增加文章标签标签
@admin.post('/tag/add', response_model=schemas.Admin_Tag_Add, summary='增加文章标签')
def admin_tag_add(tag: schemas.Admin_Tag_Add, db: Session = Depends(get_db),
                  user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_tag_add(db=db, tag=tag)


# 根据文章标签标签id查询文章标签标签
@admin.get('/tag/edit/{tag_id}', response_model=schemas.Admin_Tag_Get, summary='查询文章标签')
def admin_tag_by_id(tag_id: int, db: Session = Depends(get_db),
                    user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_tag_by_id(db=db, tag_id=tag_id)


# 修改文章标签标签
@admin.put('/tag/edit/{tag_id}', response_model=schemas.Admin_Tag_Add, summary='修改文章标签')
def admin_tag_edit(tag_id: int, tag: schemas.Admin_Tag_Add, db: Session = Depends(get_db),
                   user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_tag_edit(db=db, tag=tag, tag_id=tag_id)


# 删除文章标签标签
@admin.delete('/tag/delete/{tag_id}', summary='删除文章标签')
def admin_tag_edit(tag_id: int, db: Session = Depends(get_db),
                   user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    crud.admin_tag_delete(db=db, tag_id=tag_id)
    return {'msg': '文章标签删除成功'}


# 管理员评论管理
# 查询评论
@admin.get('/comment', summary='查询评论')
def admin_comment_get(page: int = 0, db: Session = Depends(get_db),
                      user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_comment_get(db=db, page=page)


#
# # 根据评论标签id查询评论标签
# @admin.get('/comment/edit/{comment_id}', response_model=schemas.Admin_Comment_Get, summary='查询评论')
# def admin_comment_by_id(comment_id: int, db: Session = Depends(get_db),
#                         user_obj: models.Blog_User = Depends(security.get_current_user)):
#     if user_obj['level'] == 1:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
#     return crud.admin_comment_by_id(db=db, comment_id=comment_id)


# 删除评论标签
@admin.delete('/comment/delete/{comment_id}', summary='删除评论')
def admin_comment_edit(comment_id: int, db: Session = Depends(get_db),
                       user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    crud.admin_comment_delete(db=db, comment_id=comment_id)
    return {'msg': '评论删除成功'}


# 管理员用户管理

# 查询用户
@admin.get('/blog_user', summary='查询用户')
def admin_blog_user_get(page: int = 0, db: Session = Depends(get_db),
                        user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_blog_user_get(db=db, page=page)


class Is_True(str, Enum):
    是 = '是'
    否 = '否'


class Gender(str, Enum):
    man = '男'
    female = '女'


# 增加用户
@admin.post('/user/add', response_model=schemas.Admin_Manager_User, summary='增加用户')
def admin_blog_user_add(username: str, password: str, gender: Gender,
                        avatar: UploadFile = None, user: schemas.User_Add_Base = None,
                        is_super_user: Is_True = '否', is_active: Is_True = '是', is_staff: Is_True = '否',
                        db: Session = Depends(get_db), user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_blog_user_add(db=db, user=user, is_super_user=is_super_user, is_active=is_active,
                                    is_staff=is_staff, username=username, password=password, gender=gender,
                                    avatar=avatar)


# 根据用户id查询用户
@admin.get('/user/edit/{user_id}', summary='查询用户')
def admin_blog_user_by_id(user_id: int, db: Session = Depends(get_db),
                          user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_blog_user_by_id(db=db, user_id=user_id)


# 修改用户
@admin.put('/user/edit/{user_id}', summary='修改用户')
def admin_blog_user_edit(user_id: int, password: str, gender: Gender,
                         avatar: UploadFile = None, signature: str = None, desc: str = None, email: str = None,
                         address: str = None, is_super_user: Is_True = '否', is_active: Is_True = '是',
                         is_staff: Is_True = '否', db: Session = Depends(get_db),
                         user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_blog_user_edit(db=db, is_super_user=is_super_user, is_active=is_active,
                                     is_staff=is_staff, user_id=user_id, password=password, gender=gender,
                                     avatar=avatar, signature=signature, desc=desc, email=email, address=address)


# 删除用户
@admin.delete('/user/delete/{user_id}', summary='删除用户')
def admin_blog_user_edit(user_id: int, db: Session = Depends(get_db),
                         user_obj: models.Blog_User = Depends(security.get_current_user)):
    if user_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户权限不足')
    return crud.admin_blog_user_delete(db=db, user_id=user_id)


# 管理员轮播图管理


# 查询轮播图
@admin.get('/img_change', summary='查询轮播图')
def admin_blog_banner_get(page: int = 0, db: Session = Depends(get_db),
                          banner_obj: models.Banner = Depends(security.get_current_user)):
    if banner_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='权限不足')
    return crud.admin_blog_banner_get(db=db, page=page)


# 增加轮播图
@admin.post('/img_add', response_model=schemas.Banner_Edit, summary='增加轮播图')
def admin_blog_banner_add(img: UploadFile, desc: str = None, url: str = None, db: Session = Depends(get_db),
                          banner_obj: models.Banner = Depends(security.get_current_user)):
    if banner_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='轮播图权限不足')
    return crud.admin_blog_banner_add(db=db, img=img, desc=desc, url=url)


# 根据轮播图id查询轮播图
@admin.get('/img_edit/{banner_id}', summary='查询轮播图')
def admin_blog_banner_by_id(banner_id: int, db: Session = Depends(get_db),
                            banner_obj: models.Banner = Depends(security.get_current_user)):
    if banner_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='轮播图权限不足')
    return crud.admin_blog_banner_by_id(db=db, banner_id=banner_id)


# 修改轮播图
@admin.put('/img_edit/{banner_id}', summary='修改轮播图')
def admin_blog_banner_edit(banner_id: int, img: UploadFile, desc: str = None, url: str = None,
                           db: Session = Depends(get_db),
                           banner_obj: models.Banner = Depends(security.get_current_user)):
    if banner_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='轮播图权限不足')
    return crud.admin_blog_banner_edit(db=db, banner_id=banner_id, img=img, desc=desc, url=url)


# 删除轮播图
@admin.delete('/img_del/{banner_id}', summary='删除轮播图')
def admin_blog_banner_edit(banner_id: int, db: Session = Depends(get_db),
                           banner_obj: models.Banner = Depends(security.get_current_user)):
    if banner_obj['level'] == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='轮播图权限不足')
    return crud.admin_blog_banner_delete(db=db, banner_id=banner_id)
