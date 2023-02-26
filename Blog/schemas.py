from enum import Enum
from typing import Optional, List, Any
from fastapi import UploadFile
from pydantic import BaseModel, Field
from datetime import datetime, date
from Blog import models

"""用户系统"""


class Gender(str, Enum):
    男 = 'man'
    女 = 'famale'


class User_Add_Base(BaseModel):
    signature: str = None
    desc: str = None
    email: str = None
    address: str = None

    class Config:
        orm_mode = True


class Update_user(BaseModel):
    signature: str = None
    desc: str = None
    gender: Gender = Field(default='男')
    email: str = None
    address: str = None

    class Config:
        orm_mode = True


class User_info(Update_user):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserAvatar(BaseModel):
    avatar: UploadFile = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    """ token """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class CreateUser(User):
    password: str

    class Config:
        orm_mode = True


"""文章系统"""


class PostPublishType(Enum):
    """ 文章发布类型
    """
    draft = 1  # 草稿
    show = 2  # 发布


class PostDetails(BaseModel):
    id: int
    title: str
    desc: str
    has_type: PostPublishType = Field(default=PostPublishType.draft)
    content: str
    category_id: int

    class Config:
        orm_mode = True


class Tags(BaseModel):
    id: int
    title: str
    desc: str
    has_type: PostPublishType = Field(default=PostPublishType.draft)
    content: str
    category_id: int

    class Config:
        orm_mode = True


class get_user_comments(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

    class Config:
        orm_mode = True


# 管理员管理用户信息
class Admin_Manager_User(Update_user):
    username: str
    is_super_user: int
    is_active: int
    is_staff: int

    class Config:
        orm_mode = True


# 管理员查询用户信息
class Admin_Manager_User_Info(Admin_Manager_User):
    id: int

    class Config:
        orm_mode = True


# 管理员查询用户信息
class Admin_Manager_User_Info_gen(Admin_Manager_User_Info):
    gender: Gender

    class Config:
        orm_mode = True


class Admin_Category_Add(BaseModel):
    name: str
    icon: str = None

    class Config:
        orm_mode = True


class Admin_Category_Get(Admin_Category_Add):
    id: int
    add_date: datetime
    pub_date: datetime

    class Config:
        orm_mode = True


class Category(str, Enum):
    category_id = models.Category.name


class Admin_Article_Add(BaseModel):
    title: str = None
    desc: str = None
    has_type: PostPublishType = Field(default=PostPublishType.draft)
    content: str = None

    class Config:
        orm_mode = True


class Admin_Article_Get(Admin_Article_Add):
    id: int
    add_date: datetime
    pub_date: datetime

    class Config:
        orm_mode = True


"""文章标签"""


class Admin_Tag_Add(BaseModel):
    name: str = None

    class Config:
        orm_mode = True


class Admin_Tag_Get(Admin_Tag_Add):
    id: int
    add_date: datetime
    pub_date: datetime

    class Config:
        orm_mode = True


"""评论管理"""


class Admin_Comment_Add(BaseModel):
    content: str = None

    class Config:
        orm_mode = True


class Admin_Comment_Get(Admin_Comment_Add):
    id: int
    user_id: int
    post_id: int
    add_date: datetime
    pub_date: datetime

    class Config:
        orm_mode = True


class CodeEnum(int, Enum):
    """业务状态码"""
    SUCCESS = 200
    FAIL = 400


class ResponseBasic(BaseModel):
    code: CodeEnum = Field(default=CodeEnum.SUCCESS, description="业务状态码 200 是成功, 400 是失败")
    data: Any = Field(default=None, description="数据结果")
    msg: str = Field(default="请求成功", description="提示")


class Response200(ResponseBasic):
    pass


class ResponseToken(Response200):
    access_token: str
    token_type: str = Field(default="bearer")


class Response400(ResponseBasic):
    code: CodeEnum = CodeEnum.FAIL
    msg: str = "请求失败"


class Banner_Edit(BaseModel):
    img: str
    desc: str = None
    url: str = None

    class Config:
        orm_mode = True


class Banner_Get(Banner_Edit):
    id: str
    add_date: datetime
    pub_date: datetime

    class Config:
        orm_mode = True
