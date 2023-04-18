from typing import Optional
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends, responses
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from db_connect import get_session
templates = Jinja2Templates(directory='./templates')
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
async def get_customers(request: Request, db: Session = Depends(get_session)):
  smth = select(Customers)
  result = db.exec(smth).all()
  return {"customers":result}

@router.post(path='/customers', response_class=HTMLResponse)
async def update_customers(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('_method')
  key = form_data.get('id')
  
  if action == 'DELETE':
    statement = select(Customers).where(Customers.customer_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError as e:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='POST':
    customer = Customers(form_data)
    db.add(customer)
    db.commit()
  elif action == 'PUT':
    print('post customers')

    statement = select(Customers).where(Customers.customer_id == key)
    customer = db.exec(statement).one()
    customer.set_value_from_form(form_data)
    
    db.add(customer)
    db.commit()
    
  smth = select(Customers)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Customers.html", {"request":request,"customers":result, "error_message":error_message})


  
