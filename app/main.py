from fastapi import FastAPI, Response , status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional, List
from random import randrange 
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session 
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependencies to session to DB



#It loops over until connection is successfully established
while True:     
    try:
        conn = psycopg.connect(host='localhost',dbname='fastapi',user='postgres',password='root123',row_factory=dict_row)
        cursor=conn.cursor()
        print("Database Connection was Successful!")
        break  
    except Exception as error:
        print("Connecting to database failed")
        print("Erro:",error)
        time.sleep(2) #sleep for 2s

my_post= [{"title": "title of post 1","content": "content of post 1", "id": 1},
          {"title":"favorite foods","content":"Indian food","id": 2}]

def find_post(id):
    for p in my_post:
        if p['id']==id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id']== id:
            return i

#Path operation
@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}


@app.get("/posts",response_model =List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return{"Data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model =schemas.Post)
def creatpost(post : schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    #new_post=cursor.fetchone() # Returns the current returned values
    #conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post} #return to user
    

@app.get("/posts/{id}", response_model =schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),)) 
    #post = cursor.fetchone()
    #print(post)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id:{id} was not found"} 
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db: Session = Depends(get_db)):
    #deleting post
    # find the index in the array that has required ID
    # my_post.pop(index)

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model =schemas.Post)
def update_post(id: int,updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    #updated_post= cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return {"data":post_query.first()}


