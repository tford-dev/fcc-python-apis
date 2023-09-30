from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from typing import Optional;
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#pydantic
#schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #Optional is from the typing library
    rating: Optional[int] = None 

#uvicorn main:app --reload 
#command above starts the local server

#temporary in-memory-database
my_posts = [
    {"title" : "title of post 1", "content" : "content of post 1", "id" : 1},
    {"title" : "Kendall is the best", "content" : "More about Kendall", "id" : 2},
    {"title" : "We can all escape", "content" : "It's only love", "rating" : 5, "id" : 3}
]

#helper
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Why hellooooooooooo"}

@app.get("/posts")
def get_posts():
    #fastapi converts data in my_posts array into json
    return {"data" : my_posts}

#Below you can see how to set the default status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}
    #title str, content str

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post: 
        #String is what gets sent back to user in json
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id: {id} was not found."}
    return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #delete the post brah
    #post_to_delete = find_post(id)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    my_posts.pop(index)
    #purpose of line below is to eliminate errors in logs
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#post parameter continue to uses schema 
@app.put("/posts/{id}")
def update_post(id: int, post: Post ):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data' : post_dict}