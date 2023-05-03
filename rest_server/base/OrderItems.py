from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from db_connect import get_session
import json
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

@router.get(path='/api/order_items', response_class=JSONResponse)
async def get_order_items(db: Session = Depends(get_session)):
  smth = select(OrderItems, Orders.Orders, Products.Products).join(Orders.Orders).join(Products.Products)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  orders = db.exec(select(Orders.Orders)).all()
  print(result)
  return {"order_items":result, "products":products, "orders":orders}

@router.delete(path='/api/order_items/{ord_it_id}', response_class=JSONResponse)
async def delete_order_items(ord_it_id: int, db: Session = Depends(get_session)):
  error = ""
  ord_it_id = int(ord_it_id)
  statement = select(OrderItems).where(OrderItems.order_item_id == ord_it_id)
  result = db.exec(statement).one()
  try:
    db.delete(result)
    db.commit()
  except IntegrityError:
    db.rollback()
    error = ERROR_MESSAGE
    
  smth = select(OrderItems, Orders.Orders, Products.Products).join(Orders.Orders).join(Products.Products)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  orders = db.exec(select(Orders.Orders)).all()
  return {"order_items":result, "products":products, "orders":orders, "error_message":error}

@router.put(path='/api/order_items/{ord_it_id}', response_class=JSONResponse)
async def update_order_items(request: Request, ord_it_id: int, db: Session = Depends(get_session)):
  form_data = json.loads(await request.body())
  statement = select(OrderItems).where(OrderItems.order_item_id == ord_it_id)
  order_items = db.exec(statement).one()
  order_items.set_value_from_form(form_data)
  
  db.add(order_items)
  db.commit()
  
  smth = select(OrderItems, Orders.Orders, Products.Products).join(Orders.Orders).join(Products.Products)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  orders = db.exec(select(Orders.Orders)).all()

  return {"order_items":result, "products":products, "orders":orders}

@router.put(path='/api/order_items', response_class=JSONResponse)
async def add_order_items(request: Request, db: Session = Depends(get_session)):
  form_data = json.loads(await request.body())

  order_items = OrderItems(form_data)
  db.add(order_items)
  db.commit()
    
  smth = select(OrderItems, Orders.Orders, Products.Products).join(Orders.Orders).join(Products.Products)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  orders = db.exec(select(Orders.Orders)).all()

  return {"order_items":result, "products":products, "orders":orders}
  


  
  
