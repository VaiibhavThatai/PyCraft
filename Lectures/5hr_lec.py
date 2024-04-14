# MAIN.PY:
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

import psycopg2 as psy
from psycopg2.extras import RealDictCursor
import time

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI()

# This command as it is in main file to create the model
# This is enough to build the model and create the table
models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


# An extra path operation to check
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    # Gives a normal sql query
    # posts = db.query(models.Post)
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    # A better way of doing the above line is:
    # print(post.dict())

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # curr_post = cursor.fetchone()

    curr_post = db.query(models.Post).filter(models.Post.id == id).first()
    print(curr_post)

    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return {"post details": curr_post}


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[-1]
#     return {"details of latest": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # print(deleted_post)
    # conn.commit()
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


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )

    # updated_post = cursor.fetchone()
    # conn.commit()

    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    if not update_post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    # If the post exists, we have to send all the new data
    update_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return {"data": update_post_query.first()}



# DATABASE.PY:
# importing statements
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Vaibhav.010402@localhost/fastapi'

# Creating the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session to talk to the database
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# The function to set up the session for sql to be executed and db connection to be closed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# All models extend this base class
Base = declarative_base()

# MODELS.PY:

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
    


