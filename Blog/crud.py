from enum import IntEnum

from fastapi import UploadFile
from sqlalchemy.orm import Session
from Blog import models, schemas
from Blog.until.file_upload import upload_file_one
from Blog.until.get_md5 import get_md5
import re


# 获取首页文章分类
def get_index_category(db: Session):
    return db.query(models.Category).order_by(-models.Category.pub_date).limit(6).all()


# 获取首页文章
def get_index_post(db: Session, skip: int = 1, limit: int = 3):
    return db.query(models.Post).order_by(-models.Post.pub_date).offset(skip).limit(limit).all()


# 获取首页左上的标签
def get_index_tag(db: Session, limit: int = 3):
    return db.query(models.Tag).order_by(-models.Tag.pub_date).limit(limit).all()


# 获取首页轮播图的图片
def get_index_img(db: Session, limit: int = 3):
    return db.query(models.Banner).order_by(-models.Banner.pub_date).limit(limit).all()


# 验证用户登录
def check_user(db: Session, username: str, password: str):
    return db.query(models.Blog_User).filter(models.Blog_User.username == username,
                                             models.Blog_User.password == password).first()


# 用户注册
def user_register(db: Session, user: schemas.CreateUser):
    user.password = get_md5(user.password)
    db_user = models.Blog_User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user


# 检查用户是否已经注册
def get_user_by_username(db: Session, username: str):
    return db.query(models.Blog_User).filter(models.Blog_User.username == username).first()


# 验证用户是否正确
# def get_user_by_username(db: Session, username: str, password: str):
#     return db.query(models.Blog_User).filter(models.Blog_User.username == username).first()


# 通过user_id查询用户信息
def get_user_by_user_id(db: Session, user_id: int):
    return db.query(models.Blog_User).filter(models.Blog_User.id == user_id).first()


# 获取用户评论通过用户
def get_user_comments(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Comment).filter(models.Comment.user_id == user_id).order_by(-models.Comment.pub_date).offset(
        skip).limit(limit).all()


# 获取用户评论通过评论id
def get_user_comments_by_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


# 删除用户评论
def delete_user_comments(db: Session, comment_id: int):
    comment_info = db.query(models.Comment).get(comment_id)
    db.delete(comment_info)
    db.commit()
    return {"msg": 1}


# 通过用户评论查看文章
def get_user_comments_by_post(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Comment).filter(models.Comment.user_id == user_id).order_by(-models.Comment.pub_date).offset(
        skip).limit(limit).all()


# 修改用户头像
def modify_user_avatar(db: Session, user_id: int, filename: str):
    user_info = db.query(models.Blog_User).get(user_id)
    user_info.avatar = filename
    db.commit()
    return user_info


# 修改用户信息
def modify_user_info(db: Session, user: schemas.User_info, username: str):
    user_info = db.query(models.Blog_User).filter(models.Blog_User.username == username).first()
    user_info.signature = user.signature
    user_info.desc = user.desc
    user_info.gender = user.gender
    user_info.email = user.email
    user_info.address = user.address
    db.commit()
    return user_info


# 获取文章内容评论和首页最新文章、文章标签、归档选项
def get_post_detail(db: Session, post_id: int, page: int = 0):
    post_detail = db.query(models.Post).filter(models.Post.id == post_id).first()
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_detail.id).offset(page).limit(10).all()
    newst_post = db.query(models.Post).order_by(-models.Post.pub_date).limit(3).all()
    tags = db.query(models.Tag).order_by(-models.Tag.pub_date).limit(6).all()
    post_dates = db.query(models.Post).order_by(models.Post.pub_date)
    dates = set([post.add_date.strftime("%Y年%m月") for post in post_dates])
    content = {
        "post_detail": post_detail,
        "comments": comments,
        "newst_post": newst_post,
        "tags": tags,
        "dates": dates
    }
    return content


# 搜索文章
def search_posts_by_title(db: Session, q: str, page: int = 0):
    return db.query(models.Post).filter(models.Post.title.like(f'%{q}%')).order_by(-models.Post.pub_date).offset(
        page).limit(10).all()


# 根据日期归档检索文章
def archive(db: Session, date: str, page: int = 0):
    dates = re.findall(string=date, pattern=r'(\d{4})\w+(\d{2})')
    start_date = dates[0][0] + '-' + dates[0][1] + '-' + '01'
    end_date_list = []
    end_date = ''
    if dates[0][1] == '12':
        end_date_list.append(str(int(dates[0][0]) + 1))
        end_date_list.append('01')
    else:
        end_date_list.append(dates[0][0])
        end_date_list.append(str(int(dates[0][1]) + 1))
    end_date = end_date_list[0] + '-' + end_date_list[1] + '-' + '01'
    archive_posts = db.query(models.Post).filter(models.Post.add_date >= start_date,
                                                 models.Post.add_date <= end_date).order_by(
        -models.Post.add_date).offset(page).limit(10).all()
    return archive_posts


# 根据标签获取文章
def get_post_by_tag(db: Session, tag_id: int, page: int = 0):
    post_id_list_by_tag = db.query(models.Tags).filter(models.Tags.tag_id == tag_id).order_by(
        -models.Tags.post_id).offset(page).limit(10).all()
    post_id_list = [i.post_id for i in post_id_list_by_tag]
    post_brief = db.query(models.Post).filter(models.Post.id.in_(post_id_list)).order_by(
        -models.Post.pub_date).offset(page).limit(10).all()
    content = {
        'post_brief': post_brief,
        'post_id_list': post_id_list
    }
    return content


# 获取文章评论
def get_post_comment(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).all()


# 管理员首页
def admin_index(db: Session):
    post_count = db.query(models.Post).count()
    user_count = db.query(models.Blog_User).count()
    comment_count = db.query(models.Comment).count()
    content = {
        'post_count': post_count,
        'user_count': user_count,
        'comment_count': comment_count
    }
    return content


# 管理员页面分类管理
def admin_category_get(db: Session, page: int = 0):
    return db.query(models.Category).order_by(-models.Category.pub_date).offset(page).limit(10).all()


# 管理员页面增加分类
def admin_category_add(db: Session, category: schemas.Admin_Category_Add):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    return db_category


# 管理员页面分类管理查询
def admin_category_by_id(category_id: int, db: Session):
    return db.query(models.Category).get(category_id)


# 管理员页面修改分类
def admin_category_edit(db: Session, category: schemas.Admin_Category_Add, category_id: int):
    db_category = db.query(models.Category).get(category_id)
    db_category.name = category.name
    db_category.icon = category.icon
    db.commit()
    return db_category


# 管理员页删除分类
def admin_category_delete(db: Session, category_id: int):
    db_category = db.query(models.Category).get(category_id)
    db.delete(db_category)
    db.commit()
    return db_category


"""文章管理"""


# 根据文章查询category
def post_category(db: Session):
    category = db.query(models.Category).all()
    category_dict = {}
    for i in category:
        category_dict[i.id] = i.name
    return category_dict


# 管理员页面文章管理

def admin_article_get(db: Session, page: int = 0):
    return db.query(models.Post).order_by(-models.Post.pub_date).offset(page).limit(10).all()


class PostPublishType(IntEnum):
    """ 文章发布类型
    """
    draft = 1  # 草稿
    show = 2  # 发布


# 管理员页面增加文章
def admin_article_add(db: Session, article: schemas.Admin_Category_Add, category_id: str):
    db_article = models.Post(**article.dict())
    string = str(db_article.has_type)[16:]
    if string == 'draft':
        num = 1
    else:
        num = 2
    category_info = db.query(models.Category).filter(models.Category.name == category_id).first()
    db_article.has_type = num
    db_article.category_id = category_info.id
    db.add(db_article)
    db.commit()
    return db_article


# 管理员页面文章管理查询
def admin_article_by_id(article_id: int, db: Session):
    return db.query(models.Post).get(article_id)


# 管理员页面修改文章
def admin_article_edit(db: Session, article: schemas.Admin_Article_Add, article_id: int):
    db_article = db.query(models.Post).get(article_id)
    db_article.title = article.title
    db_article.desc = article.desc
    db_article.content = article.content
    if article.has_type == 'PostPublishType.draft':
        db_article.has_type = 1
    else:
        db_article.has_type = 2
    db.commit()
    return db_article


# 管理员页删除文章
def admin_article_delete(db: Session, article_id: int):
    db_category = db.query(models.Post).get(article_id)
    db.delete(db_category)
    db.commit()
    return db_category


"""文章标签管理"""


# 管理员页面文章标签管理

def admin_tag_get(db: Session, page: int = 0):
    return db.query(models.Tag).order_by(-models.Tag.pub_date).offset(page).limit(10).all()


# 管理员页面增加文章标签
def admin_tag_add(db: Session, tag: schemas.Admin_Tag_Add):
    db_tag = models.Tag(**tag.dict())
    db_tag.name = tag.name
    db.add(db_tag)
    db.commit()
    return db_tag


# 管理员页面文章标签管理查询
def admin_tag_by_id(tag_id: int, db: Session):
    return db.query(models.Tag).get(tag_id)


# 管理员页面修改文章标签
def admin_tag_edit(db: Session, tag: schemas.Admin_Tag_Add, tag_id: int):
    db_tag = db.query(models.Tag).get(tag_id)
    db_tag.name = tag.name
    db.commit()
    return db_tag


# 管理员页删除文章标签
def admin_tag_delete(db: Session, tag_id: int):
    db_tag = db.query(models.Tag).get(tag_id)
    db.delete(db_tag)
    db.commit()
    return db_tag


"""评论管理"""


# 管理员页面评论管理

def admin_comment_get(db: Session, page: int = 0):
    comments = db.query(models.Comment).order_by(-models.Comment.pub_date).offset(page).limit(10).all()
    post_list = []
    for i in comments:
        post = db.query(models.Post).get(i.post_id)
        post_list.append(post.title)
    content = {'comments': comments, 'post_list': post_list}
    return content


#
# # 管理员页面评论管理文章查询
# def admin_post_by_comment(comment_id: int, db: Session):
#     return db.query(models.Comment).get(comment_id)


# 管理员页删除评论
def admin_comment_delete(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).get(comment_id)
    db.delete(db_comment)
    db.commit()
    return db_comment


"""用户管理"""


# 管理员页面用户管理

def admin_blog_user_get(db: Session, page: int = 0):
    return db.query(models.Blog_User).order_by(-models.Blog_User.pub_date).offset(page).limit(10).all()


# 管理员页面增加用户
def admin_blog_user_add(db: Session, username: str, password: str, gender: str, avatar: UploadFile,
                        user: schemas.Admin_Manager_User_Info,
                        is_super_user: str = '否', is_active: str = '是', is_staff: str = '否'):
    if is_super_user == '否':
        is_super_user = 0
    else:
        is_super_user = 1
    if is_active == '否':
        is_active = 0
    else:
        is_active = 1
    if is_staff == '否':
        is_staff = 0
    else:
        is_super_user = 1
    file_avatar = upload_file_one(avatar)
    filename = file_avatar['filename']
    password = get_md5(password)
    gender = str(gender)[7:]
    db_blog_user = models.Blog_User(is_super_user=is_super_user, is_active=is_active, is_staff=is_staff,
                                    avatar=filename, username=username, password=password, gender=gender, **user.dict())
    db.add(db_blog_user)
    db.commit()
    return db_blog_user


# 管理员页面用户管理查询
def admin_blog_user_by_id(user_id: int, db: Session):
    return db.query(models.Blog_User).get(user_id)


# 管理员页面修改用户
def admin_blog_user_edit(db: Session, user_id: int, password: str, gender: str, avatar: UploadFile,
                         signature: str, desc: str, email: str, address: str,
                         is_super_user: str = '否', is_active: str = '是', is_staff: str = '否'):
    user_info = db.query(models.Blog_User).get(user_id)
    user_info.password = get_md5(password)
    gender = str(gender)[7:]
    user_info.gender = gender
    file_avatar = upload_file_one(avatar)
    filename = file_avatar['filename']
    user_info.avatar = filename
    if is_super_user == '否':
        is_super_user = 0
    else:
        is_super_user = 1
    if is_active == '否':
        is_active = 0
    else:
        is_active = 1
    if is_staff == '否':
        is_staff = 0
    else:
        is_super_user = 1
    password = get_md5(password)
    user_info.password = password
    user_info.is_super_user = is_super_user
    user_info.is_active = is_active
    user_info.is_staff = is_staff
    user_info.signature = signature
    user_info.desc = desc
    user_info.email = email
    user_info.address = address
    db.commit()
    return {'msg': '修改成功'}


# 管理员页删除用户
def admin_blog_user_delete(db: Session, user_id: int):
    db_blog_user = db.query(models.Blog_User).get(user_id)
    db.delete(db_blog_user)
    db.commit()
    content = {
        'db_blog_user': db_blog_user,
        'msg': '删除成功'
    }
    return content


"""轮播图管理"""


# 管理员页面轮播图查询

def admin_blog_banner_get(db: Session, page: int = 0):
    return db.query(models.Banner).order_by(-models.Banner.pub_date).offset(page).limit(10).all()


# 管理员页面增加轮播图
def admin_blog_banner_add(db: Session, img: UploadFile, desc: str = None, url: str = None):
    file_avatar = upload_file_one(img)
    filename = file_avatar['filename']
    db_banner = models.Banner(img=filename, desc=desc, url=url)
    db.add(db_banner)
    db.commit()
    return db_banner


# 管理员页面轮播图管理查询
def admin_blog_banner_by_id(banner_id: int, db: Session):
    return db.query(models.Banner).get(banner_id)


# 管理员页面修改轮播图
def admin_blog_banner_edit(db: Session, banner_id: int, img: UploadFile, desc: str = None, url: str = None):
    banner_info = db.query(models.Banner).get(banner_id)
    file_avatar = upload_file_one(img)
    filename = file_avatar['filename']
    banner_info.img = filename
    banner_info.url = url
    banner_info.desc = desc
    db.commit()
    return {'msg': '修改成功'}


# 管理员页删除轮播图
def admin_blog_banner_delete(db: Session, banner_id: int):
    db_banner = db.query(models.Banner).get(banner_id)
    db.delete(db_banner)
    db.commit()
    content = {
        'db_blog_banner': db_banner,
        'msg': '删除成功'
    }
    return content
