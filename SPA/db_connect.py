import os

from sqlmodel import Session, create_engine, select # type: ignore

user = os.getenv('POSTGRES_USERNAME') if os.getenv('POSTGRES_USERNAME') is not None else 'postgres'
password = os.getenv('POSTGRES_PASSWORD') if os.getenv('POSTGRES_PASSWORD') is not None else 'postgres'
db_host = os.getenv('POSTGRES_DB_HOST') if os.getenv('POSTGRES_DB_HOST') is not None else 'localhost'
db_name = os.getenv('POSTGRES_DB_NAME') if os.getenv('POSTGRES_DB_NAME') is not None else 'ElectroStoreDB'
conString = f"postgresql://{user}:{password}@{db_host}:5432/{db_name}"

engine = create_engine(conString) #type: ignore

def get_session():
  return Session(engine)