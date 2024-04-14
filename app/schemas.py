from pydantic import BaseModel, conint
from typing import Optional

from datetime import datetime

from pydantic import EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_model = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# Sending data from user to us
class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # for sqlalchemy model to dict
    class Config:
        orm_model = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dir: bool
    # dir : conint(ge=0, le=1)