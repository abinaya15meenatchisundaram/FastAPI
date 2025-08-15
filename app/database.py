from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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