from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date
from dateutil.parser import parse

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

  
  
