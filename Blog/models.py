from enum import IntEnum

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, func, Table, Enum, Text, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from .database import Base


class BaseModel(Base):
    __abstract__ = True
    add_date = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    pub_date = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='修改时间')


class Category(BaseModel):
    """分类模型"""
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    icon = Column(String(128), nullable=True)
    post = relationship('Post', backref='category', lazy=True)

    # 分类管理的级联删除
    # post = relationship('Post', back_populates='category', cascade='all,delete', passive_deletes=True,)

    def __repr__(self):
        return '<Category %r>' % self.name


# # 多对多关系帮助器表
# tags = Table('tags', Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
#              Column('post_id', Integer, ForeignKey('post.id'), primary_key=True))


class PostPublishType(IntEnum):
    """ 文章发布类型
    """
    draft = 1  # 草稿
    show = 2  # 发布


class Post(BaseModel):
    """文章模型"""
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    desc = Column(String(255), nullable=True)
    has_type = Column(Enum(PostPublishType), server_default='show', nullable=False)
    content = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id', ), nullable=False)

    # tags = relationship('Tag', secondary=tags, lazy='subquery', backref=backref('post', lazy=True))

    # comment = relationship('Comment', back_populates='post', cascade='all,delete', passive_deletes=True)

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(BaseModel):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class Blog_User(BaseModel):
    __tablename__ = 'blog__user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(320), nullable=False)
    avatar = Column(String(200), nullable=True)
    is_super_user = Column(Boolean, nullable=True, default=False)
    is_active = Column(Boolean, nullable=True, default=True)
    is_staff = Column(Boolean, nullable=True, default=False)
    signature = Column(String(100), nullable=True)
    desc = Column(String(150), nullable=True)
    gender = Column(String(30), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(100), nullable=True)

    # comment = relationship('Comment', backref='user', lazy='True')

    def __repr__(self):
        return '<Category %r>' % self.username


class Banner(BaseModel):
    __tablename__ = 'banner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    img = Column(String(200), nullable=False)
    desc = Column(String(200), nullable=True)
    url = Column(String(300), nullable=True)

    # def __repr__(self):
    # return f'{self.id}=>{self.img}+{self.url}'
    # return f'{self.img}, {self.url}'


class Comment(BaseModel):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(200), nullable=True)
    # post = relationship('Post', ForeignKey('post.id'))
    user = relationship('Blog_User', backref='comment')
    post = relationship('Post', backref='comment')
    # user = relationship('Blog_User')
    user_id = Column(Integer, ForeignKey(Blog_User.id, ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    # post = relationship('Post', back_populates='comment')

    # 　　posts = relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return self.content


class Tags(Base):
    __tablename__ = 'tags'
    tag_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, primary_key=True)
