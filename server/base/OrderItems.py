from typing import Optional
from sqlmodel import Field, SQLModel

class OrderItemsModel(SQLModel):
  order_item_id : Optional[int] = Field(default=None, primary_key=True)
  order_id : Optional[int] = Field(default=None, foreign_key="orders.order_id")
  product_id : Optional[int] = Field(default=None, foreign_key="products.product_id")
  quantity : int
  price : float
  
  
class OrderItems(OrderItemsModel, table=True):
  __tablename__ : str = 'order_items'

  
  
