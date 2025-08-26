from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time

#Connection String
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root123@localhost/fastapi'

#Responsible to SQLAlchemy connection to postgres DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Talk to DB we need session
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
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

"""