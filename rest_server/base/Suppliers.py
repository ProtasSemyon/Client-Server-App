from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends, responses
from fastapi.responses import HTMLResponse, JSONResponse
from db_connect import get_session

import json
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

@router.get(path='/api/suppliers', response_class=JSONResponse)
async def get_suppliers(db: Session = Depends(get_session)):
  smth = select(Suppliers)
  result = db.exec(smth).all()
  return {"suppliers":result}

@router.delete(path='/api/suppliers/{supp_id}', response_class=JSONResponse)
async def delete_supplier(supp_id: int, db: Session = Depends(get_session)):
  error = ""
  statement = select(Suppliers).where(Suppliers.supplier_id == supp_id)
  result = db.exec(statement).one()
  try:
    db.delete(result)
    db.commit()
  except IntegrityError as e:
    db.rollback()
    error = ERROR_MESSAGE
    
  smth = select(Suppliers)
  result = db.exec(smth).all()
  return {"suppliers":result, "error_message":error}

@router.put(path='/api/suppliers/{supp_id}')
async def update_supplier(supp_id: int, request: Request, db: Session = Depends(get_session)):
  form_data = json.loads(await request.body())
  
  statement = select(Suppliers).where(Suppliers.supplier_id == supp_id)
  supplier = db.exec(statement).one()
  supplier.set_value_from_form(form_data)
  
  db.add(supplier)
  db.commit()
  
  smth = select(Suppliers)
  result = db.exec(smth).all()
  return {"suppliers":result}
    

@router.put(path='/api/suppliers', response_class=JSONResponse)
async def add_supplier(request: Request, db: Session = Depends(get_session)):
  form_data = json.loads(await request.body())

  supplier = Suppliers(form_data)
  db.add(supplier)
  db.commit()
    
  smth = select(Suppliers)
  result = db.exec(smth).all()
  return {"suppliers":result}
