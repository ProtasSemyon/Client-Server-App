from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from db_connect import get_session
ERROR_MESSAGE = "You can't delete this row: it has connections with other tables"

from sqlmodel import Field, SQLModel
from datetime import date
from dateutil.parser import parse
from base import Customers

class OrdersModel(SQLModel):
  order_id : Optional[int] = Field(default=None, primary_key=True)
  order_date : date
  total_amount : float
  customer_id : Optional[int] = Field(default=None, foreign_key="customers.customer_id")
  
class Orders(OrdersModel, table=True):
    __tablename__ : str = 'orders'
    
    def __init__(self, form_data):
      self.set_value_from_form(form_data)
  
    def set_value_from_form(self, form_data):
      self.order_date = parse(form_data.get('order_date'))
      self.total_amount = float(form_data.get('total_amount'))
      self.customer_id = int(form_data.get('customer_id'))
      
router = APIRouter()

@router.get(path='/api/orders', response_class=JSONResponse)
async def get_orders(db: Session = Depends(get_session)):
  smth = select(Orders, Customers.Customers).join(Customers.Customers)
  result = db.exec(smth).all()
  customers = db.exec(select(Customers.Customers)).all()
  return {"orders":result, "customers":customers}

@router.delete(path='/api/orders/{order_id}')
async def delete_order(order_id: int, db: Session = Depends(get_session)):
  error = ""
  order_id = int(order_id)
  statement = select(Orders).where(Orders.order_id == order_id)
  result = db.exec(statement).one()
  try:
    db.delete(result)
    db.commit()
  except IntegrityError:
    db.rollback()
    error = ERROR_MESSAGE
    
  smth = select(Orders, Customers.Customers).join(Customers.Customers)
  result = db.exec(smth).all()
  customers = db.exec(select(Customers.Customers)).all()
  return {"orders":result, "customers":customers, "error_message":error}

@router.put(path='/api/orders/{order_id}', response_class=JSONResponse)
async def update_order(request: Request, order_id: int, db: Session = Depends(get_session)):
  form_data = await request.form()
  
  statement = select(Orders).where(Orders.order_id == order_id)
  order = db.exec(statement).one()
  order.set_value_from_form(form_data) # type: ignore
  
  db.add(order)
  db.commit()
  
  smth = select(Orders, Customers.Customers).join(Customers.Customers)
  result = db.exec(smth).all()
  customers = db.exec(select(Customers.Customers)).all()
  return {"orders":result, "customers":customers}

@router.put(path='/api/orders', response_class=JSONResponse)
async def pdate_orders(request: Request, db: Session = Depends(get_session)):
  form_data = await request.form()
  order = Orders(form_data)
  db.add(order)
  db.commit()
    
  smth = select(Orders, Customers.Customers).join(Customers.Customers)
  result = db.exec(smth).all()
  customers = db.exec(select(Customers.Customers)).all()
  return {"orders":result, "customers":customers}


  
  
