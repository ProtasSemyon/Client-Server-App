from typing import Optional
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends, responses
from fastapi.responses import HTMLResponse, JSONResponse
from db_connect import get_session
templates = Jinja2Templates(directory='./templates')
ERROR_MESSAGE = "You can't delete this row: it has connections with other tables"

from sqlmodel import Field, SQLModel

class SuppliersModel(SQLModel):
  supplier_id : Optional[int] = Field(default=None, primary_key=True)
  supplier_name : str
  contact_name : str
  email : str
  phone : str
  
  
class Suppliers(SuppliersModel, table=True):
  __tablename__ : str = 'suppliers'
  
  def __init__(self, form_data):
    self.set_value_from_form(form_data)
  
  def set_value_from_form(self, form_data):
    self.supplier_name = str(form_data.get('supplier_name'))
    self.contact_name = str(form_data.get('contact_name'))
    self.email = str(form_data.get('email'))
    self.phone = str(form_data.get('phone'))

router = APIRouter()

@router.get(path='/suppliers', response_class=JSONResponse)
async def get_suppliers(request: Request, db: Session = Depends(get_session)):
  smth = select(Suppliers)
  result = db.exec(smth).all()
  return {"request":request,"suppliers":result}

@router.post(path='/suppliers', response_class=HTMLResponse)
async def update_suppliers(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(Suppliers).where(Suppliers.supplier_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError as e:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    supplier = Suppliers(form_data)
    db.add(supplier)
    db.commit()
  elif action == '/update':
    statement = select(Suppliers).where(Suppliers.supplier_id == key)
    supplier = db.exec(statement).one()
    supplier.set_value_from_form(form_data)
    
    db.add(supplier)
    db.commit()
    
  smth = select(Suppliers)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Suppliers.html", {"request":request,"suppliers":result, "error_message":error_message})
