# & MAIN.PY

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

import psycopg2 as psy
from psycopg2.extras import RealDictCursor
import time

from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends

from typing import List

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


while True:
    try:
        conn = psy.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="Vaibhav.010402",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection is successful")
        break
    except Exception as e:
        print("Connection to database failed")
        print("Error: ", e)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Success Success Success!!!"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_posts(id: int, db: Session = Depends(get_db)):
    curr_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return curr_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    if not delete_post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )

    # if exits lets delete
    delete_post_query.delete(synchronize_session=False)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# & UPDATE:
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    if not update_post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    # If the post exists, we have to send all the new data
    update_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_post_query.first()

# & MODELS.PY

# import base that we created from database file
from .database import Base

# to create column
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


# class Post extends Base
class Post(Base):
    # we can set up the table name
    __tablename__ = "posts"

    # creating columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # This is wrong, default = True won't be useful.
    # published = Column(Boolean, default=True)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    # This is how we create timestamp column in sqlalchemy
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default=text('now()') )
    
class User(Base):
    __tablename__ = 'users'
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    id = Column(Integer, nullable = False, primary_key= True)
    created_at = Column(TIMESTAMP (timezone = True), nullable = False, server_default=text('now()'))
                        
    

# & SCHEMAS.PY:
from pydantic import BaseModel
from typing import Optional

from datetime import datetime

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# Sending data from user to us
class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass

# Direction from us to user
# class PostResponse(BaseModel):
    # title: str
    # content: str
    # published: bool
    # # we are not sending the id and created_at field
    
    # & EXTRA POINT
    # # for timestamp, type =??
    # created_at: datetime
    
    # # for sqlalchemy model to dict
    # class Config:
    #     orm_model = True

# ANOTHER WAY
class PostResponse(PostBase):
    
    id: int
    created_at: datetime
    
    # for sqlalchemy model to dict
    class Config:
        orm_model = True
        

# & DATABASE.PY: NO CHANGE FROM 5hr_lec.py