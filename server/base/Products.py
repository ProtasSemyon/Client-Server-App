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