import os

from sqlmodel import Session, create_engine, select # type: ignore

user = os.getenv('POSTGRES_USERNAME')
password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_DB_HOST')
db_name = os.getenv('POSTGRES_DB_NAME')
conString = f"postgresql://{user}:{password}@{db_host}:5432/{db_name}"

engine = create_engine(conString)

def get_session():
  return Session(engine)