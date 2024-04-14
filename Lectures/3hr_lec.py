from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title":"Post 1", "content": "content of post 1", "id": 1}, {"title":"Post 2", "content": "content of post 2", "id": 2}]

def findPost(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

def findIdPost(id):
    for i, p in enumerate(my_posts):
        if(p['id'] == id):
            return i

@app.get("/")
async def root():
    return {"message": "Success Success Success!!!"}


@app.get('/posts')
def get_posts():
    return {"data": my_posts}


@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get('/posts/{id}')
def get_posts(id: int):
    
    post = findPost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return {"post details": post}

@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[-1]
    return {"details of latest": post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # logic for deleting a post
    # figuring out which specific within the array has the id 
    
    # find the index in the array which has the required id. 
    # my_posts.pop(index) -> Pretty simple
    index = findIdPost(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} does not exist")

    my_posts.pop(index)
    return {"Message" : "Post deleted successfully!!!"}


# & UPDATE:

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    
    # find the post
    index = findIdPost(id)
        
    if not index: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} not found")
    
    post_dict = post.dict()
    post_dict['id'] = id
    
    # update in the list at that index
    my_posts[index] = post_dict
    return {"data" : post_dict}

 
