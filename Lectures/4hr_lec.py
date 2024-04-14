from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2 as psy
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


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

my_posts = [
    {"title": "Post 1", "content": "content of post 1", "id": 1},
    {"title": "Post 2", "content": "content of post 2", "id": 2},
]


def findPost(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None


def findIdPost(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Success Success Success!!!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    
    # Always avoid the f string method, as it is vulnerable to SQL injection
    # cursor.execute(f"""INSERT INTO posts (title, content, published) VALUES {post.title}, {post.content}, {post.published})""")
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    curr_post = cursor.fetchone()
    if not curr_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    return {"post details": curr_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"details of latest": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    print(deleted_post)
    if not deleted_post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id = {id} not found"
        )
         
    conn.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


# & UPDATE:

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
         
    conn.commit()
    return {"data": updated_post}
