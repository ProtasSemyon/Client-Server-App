from typing import Optional
from sqlmodel import Field, SQLModel

class ProductSuppliersModel(SQLModel):
  product_supplier_id : Optional[int] = Field(default=None, primary_key=True)
  supplier_id : Optional[int] = Field(default=None, foreign_key="suppliers.supplier_id")
  product_id : Optional[int] = Field(default=None, foreign_key="products.product_id")
  price : float
  
  
class ProductSuppliers(ProductSuppliersModel, table=True):
  __tablename__ : str = 'suppliers'