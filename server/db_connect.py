import os

from sqlmodel import Session, create_engine, select # type: ignore

user = os.getenv('POSTGRES_USERNAME')
conString = f"postgresql://{user}:postgres@localhost:5432/ElectroStoreDB"

engine = create_engine(conString)

def get_session():
  return Session(engine)