from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from db_connect import get_session
import json
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

@router.get(path='/api/products', response_class=JSONResponse)
async def get_products(db: Session = Depends(get_session)):
  smth = select(Products)
  result = db.exec(smth).all()
  return {"products":result}

@router.delete(path='/api/products/{product_id}', response_class=JSONResponse)
async def delete_product(product_id: int, db: Session = Depends(get_session)):
  error = ""
  statement = select(Products).where(Products.product_id == product_id)
  result = db.exec(statement).one()
  try:
    db.delete(result)
    db.commit()
  except IntegrityError as e:
    db.rollback()
    error = ERROR_MESSAGE
    
  smth = select(Products)
  result = db.exec(smth).all()
  return {"products":result, "error_message":error}

@router.put(path='/api/products/{product_id}', response_class=JSONResponse)
async def update_product(request: Request, product_id: int, db: Session = Depends(get_session)):
  form_data = json.loads(await request.body())
  
  statement = select(Products).where(Products.product_id == product_id)
  products = db.exec(statement).one()
  products.set_value_from_form(form_data)
  
  db.add(products)
  db.commit()
  
  smth = select(Products)
  result = db.exec(smth).all()
  return {"products":result}

@router.put(path='/api/products', response_class=JSONResponse)
async def add_product(request: Request, db: Session = Depends(get_session)):
  form_data = json.loads(await request.body())
  products = Products(form_data)
  db.add(products)
  db.commit()
    
  smth = select(Products)
  result = db.exec(smth).all()
  return {"products":result}
