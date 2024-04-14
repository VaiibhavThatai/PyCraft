from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

# Create a new instance of the FastAPI 
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    # adding an optional parameter
    published: bool = True
    # creating a complete optional with default value as None
    rating: Optional[int] = None



#& Known as Path Operation and something referred as route

#^ This is a decorator
# We have applied it to a function
# This decorator is responsible for making that function act as an API
# app as the name of our fastAPI instance and get request is made. 
@app.get("/")
# This function is a normal python function
# Async keyword is when we want to do something that takes time and 
# like we want to do it asynchronously.
async def root():
    # fastAPI will automatically convert this dictionary to JSON
    return {"message": "Success Success Success!!!"}

# Name the path operation functions as logical as possible
# JSON is the language of APIs
@app.get('/posts')
def get_posts():
    return {"data": "This is your posts"}

# @app.post("/createposts")
# def create_post():

# @app.post("/createposts")
# # store all the data in the Body in a dictionary and store it in the argument payload
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     # Now we also sending data back to user
#     return {"new_post": f"title: {payload['title']} content: {payload['content']}"}

@app.post('/createposts')
# as we mention the pydantic class Post here, fastAPI will check for the constraints
# It will check where the new_post has the required content in correct data type or not
# It automatically accesses the data
def create_post(new_post: Post):
    print(new_post)
    # print(new_post.published)
    print(new_post.dict())
    return {"data": "post"}
# Now we want to tell the user what data do we want
# title str, content str, category, Boolean published etc.



#^ THE ORDER MATTERS
# The first path operation that matches will run
# this below will not run as theirs a path operation above with same url
# @app.get('/')
# def get_posts():
#     return {"data": "This is your posts"}


#^ To run live server we use uvicorn
# Command: uvicorn main:app

# Everytime we make a change we have to refresh
#^ To avoid that and do this automatically use the following command:
# uvicorn main:app -reload

