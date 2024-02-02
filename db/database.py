import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from dotenv import load_dotenv

load_dotenv()

DATABASE = os.environ['DATABASE']
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']
HOST = os.environ['DB_SERVER']
PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']

DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME
)

Engine = create_engine(DATABASE_URL, client_encoding='utf8', poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
