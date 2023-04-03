from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date

class OrdersModel(SQLModel):
  order_id : Optional[int] = Field(default=None, primary_key=True)
  order_date : date
  total_amount : float
  customer_id : Optional[int] = Field(default=None, foreign_key="customers.customer_id")
  
class Orders(OrdersModel, table=True):
    __tablename__ : str = 'orders'

  
  
