from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends, responses
from fastapi.responses import JSONResponse

from db_connect import get_session
ERROR_MESSAGE = "You can't delete this row: it has connections with other tables"

from sqlmodel import Field, SQLModel

class CustomersModel(SQLModel):
  customer_id :Optional[int] = Field(default=None, primary_key=True)
  first_name :str
  last_name :str
  email :str = Field(unique=True)
  phone :str
  
class Customers(CustomersModel, table=True):
  __tablename__ : str = 'customers'
  
  def __init__(self, form_data):
    self.set_value_from_form(form_data)
  
  def set_value_from_form(self, form_data):
    self.first_name = str(form_data.get('first_name'))
    self.last_name = str(form_data.get('last_name'))
    self.email = str(form_data.get('email'))
    self.phone = str(form_data.get('phone'))
    

router = APIRouter()

@router.get(path='/customers', response_class=JSONResponse)
async def get_customers(db: Session = Depends(get_session)):
  smth = select(Customers)
  result = db.exec(smth).all()
  return {"customers":result}

@router.delete(path='/customers/{customer_id}', response_class=JSONResponse)
async def delete_customer(customer_id, db: Session = Depends(get_session)):
  customer_id = int(customer_id)
  statement = select(Customers).where(Customers.customer_id == customer_id)
  result = db.exec(statement).one()
  try:
    db.delete(result)
    db.commit()
  except IntegrityError as e:
    db.rollback()
    
  smth = select(Customers)
  result = db.exec(smth).all()
  return {"customers":result, "error_message":ERROR_MESSAGE}

@router.put(path='/customers/{customer_id}', response_class=JSONResponse)
async def update_customer(request: Request, customer_id, db: Session = Depends(get_session)):
  form_data = await request.form()

  statement = select(Customers).where(Customers.customer_id == customer_id)
  customer = db.exec(statement).one()
  customer.set_value_from_form(form_data)
  
  db.add(customer)
  db.commit()
  
  smth = select(Customers)
  result = db.exec(smth).all()
  return {"customers":result}
 

@router.put(path='/customers', response_class=JSONResponse)
async def add_customer(request: Request, db: Session = Depends(get_session)):
  form_data = await request.form()
  customer = Customers(form_data)
  db.add(customer)
  db.commit()
    
  smth = select(Customers)
  result = db.exec(smth).all()
  return {"customers":result}


  
