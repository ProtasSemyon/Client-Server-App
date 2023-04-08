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
  
  def __init__(self, form_data):
    self.set_value_from_form(form_data)
  
  def set_value_from_form(self, form_data):
    self.order_id = int(form_data.get('order_id'))
    self.product_id = int(form_data.get('product_id'))
    self.quantity = int(form_data.get('quantity'))
    self.price = float(form_data.get('price'))


  
  
