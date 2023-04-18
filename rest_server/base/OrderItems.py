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
from base import Orders
from base import Products

class OrderItemsModel(SQLModel):
  order_item_id : Optional[int] = Field(default=None, primary_key=True)
  order_id : Optional[int] = Field(default=None, foreign_key="orders.order_id")
  product_id : Optional[int] = Field(default=None, foreign_key="products.product_id")
  quantity : int
  price : float
  
  
class OrderItems(OrderItemsModel, table=True):
  __tablename__ : str = 'order_items'
  
  def __init__(self, form_data):
    self.set_value_from_form(form_data)
  
  def set_value_from_form(self, form_data):
    self.order_id = int(form_data.get('order_id'))
    self.product_id = int(form_data.get('product_id'))
    self.quantity = int(form_data.get('quantity'))
    self.price = float(form_data.get('price'))
    
router = APIRouter()

@router.get(path='/order_items', response_class=JSONResponse)
async def get_order_items(request: Request, db: Session = Depends(get_session)):
  smth = select(OrderItems, Orders.Orders, Products.Products).join(Orders.Orders).join(Products.Products)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  orders = db.exec(select(Orders.Orders)).all()

  return {"order_items":result, "products":products, "orders":orders}

@router.post(path='/order_items', response_class=HTMLResponse)
async def update_order_items(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(OrderItems).where(OrderItems.order_item_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    order_items = OrderItems(form_data)
    db.add(order_items)
    db.commit()
  elif action == '/update':
    statement = select(OrderItems).where(OrderItems.order_item_id == key)
    order_items = db.exec(statement).one()
    order_items.set_value_from_form(form_data)
    db.add(order_items)
    db.commit()
    
  smth = select(OrderItems, Orders.Orders, Products.Products).join(Orders.Orders).join(Products.Products)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  orders = db.exec(select(Orders.Orders)).all()

  return templates.TemplateResponse("OrderItems.html", {"request":request,"order_items":result, "products":products, "orders":orders})
  


  
  
