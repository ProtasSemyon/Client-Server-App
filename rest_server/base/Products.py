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

class ProductsModel(SQLModel):
  product_id : Optional[int] = Field(default=None, primary_key=True)
  product_name : str
  brand : str
  category : str
  description : Optional[str]
  price : float
  stock_quantity : int
  
  
class Products(ProductsModel, table=True):
  __tablename__ : str = 'products'
  
  def __init__(self, form_data):
    self.set_value_from_form(form_data)
  
  def set_value_from_form(self, form_data):
    self.product_name=str(form_data.get('product_name'))
    self.brand=str(form_data.get('brand'))
    self.category=str(form_data.get('category'))
    self.description=str(form_data.get('description'))
    self.price=float(form_data.get('price'))    
    self.stock_quantity=int(form_data.get('stock_quantity'))
    
router = APIRouter()

@router.get(path='/products', response_class=JSONResponse)
async def get_products(request: Request, db: Session = Depends(get_session)):
  smth = select(Products)
  result = db.exec(smth).all()
  return {"products":result}

@router.post(path='/products', response_class=HTMLResponse)
async def update_products(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(Products).where(Products.product_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError as e:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    products = Products(form_data)
    db.add(products)
    db.commit()
  elif action == '/update':
    statement = select(Products).where(Products.product_id == key)
    products = db.exec(statement).one()
    products.set_value_from_form(form_data)
    
    db.add(products)
    db.commit()
    
  smth = select(Products)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Products.html", {"request":request,"products":result, "error_message":error_message})
