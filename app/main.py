from fastapi import FastAPI, Response , status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange 
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session 
from . import models, schemas,utils
from .database import engine, get_db
from .routers import post,user
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

app.include_router(post.router)
app.include_router(user.router)


#Path operation
@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}



