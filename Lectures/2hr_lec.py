from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

# Create a new instance of the FastAPI 
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    # adding an optional parameter
    published: bool = True
    # creating a complete optional with default value as None
    rating: Optional[int] = None


# CRUD Operations
# For a Social Media API, we'll need options to
# Create a Post
# Read a Post
# Update a Post
# Delete a Post

# There's a standard convention for naming 
# 1. Always use Plural.
# For Create: we'll use the POST method and will use /posts
# For Read we'll use GET method and will use two urls /posts/:id (for particular) and /posts (for multiple)
# For Update we' use PUT/PATCH method and will use the url /posts/:id
# For Delete we' use DELETE method and will use the url /posts/:id 

# PUT VS PATCH
# PUT -> all the information has to be sent 
# PATCH -> send only the field needed to be updated


# Not using database, but storing here in memory as a variable for a while
my_posts = [{"title":"Post 1", "content": "content of post 1", "id": 1}, {"title":"Post 2", "content": "content of post 2", "id": 2}]

def findPost(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

#& Known as Path Operation and something referred as route  
@app.get("/")
async def root():
    return {"message": "Success Success Success!!!"}


@app.get('/posts')
def get_posts():
    return {"data": my_posts}

# @app.post('/posts')
# def create_post(post: Post):
#     # creating the post to dict as we have a list of dictionary of posts
#     post_dict = post.dict()
#     # we add the id column to it
#     post_dict['id'] = randrange(0, 10000000)
#     # appending it to the list 
#     my_posts.append(post_dict)
#     # returning the newly created dict back to the user
#     return {"data": post_dict}

# & To also set up the status code for successful creation i.e., 201:
@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    # creating the post to dict as we have a list of dictionary of posts
    post_dict = post.dict()
    # we add the id column to it
    post_dict['id'] = randrange(0, 10000000)
    # appending it to the list 
    my_posts.append(post_dict)
    # returning the newly created dict back to the user
    return {"data": post_dict}

# Path parameter (id)
# @app.get('/posts/{id}')
# def get_posts(id):
#     print(id)
#     # Important thing to note
#     post = findPost((int)(id))
#     return {"post details": post}



# @app.get('/posts/{id}')
# def get_posts(id: int, response: Response):

#     post = findPost(id)
#     if not post:
#         response.status_code = 404
#     return {"post details": post}

# better way
# @app.get('/posts/{id}')
# def get_posts(id: int, response: Response):

#     post = findPost(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": "No such post"}
#     return {"post details": post}

@app.get('/posts/{id}')
def get_posts(id: int, response: Response):
    
    post = findPost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return {"post details": post}

# The following won't be able to run as fastAPI works in the top down order
@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[-1]
    return {"details of latest": post}
# to make this work we have to keep it above the above routing request

