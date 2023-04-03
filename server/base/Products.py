from typing import Optional
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