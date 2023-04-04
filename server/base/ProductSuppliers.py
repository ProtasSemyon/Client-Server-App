from typing import Optional
from sqlmodel import Field, SQLModel

class ProductSuppliersModel(SQLModel):
  product_supplier_id : Optional[int] = Field(default=None, primary_key=True)
  supplier_id : Optional[int] = Field(default=None, foreign_key="suppliers.supplier_id")
  product_id : Optional[int] = Field(default=None, foreign_key="products.product_id")
  
  
class ProductSuppliers(ProductSuppliersModel, table=True):
  __tablename__ : str = 'product_suppliers'
  
  def __init__(self, form_data):
    self.set_value_from_form(form_data)
  
  def set_value_from_form(self, form_data):
    self.product_id = int(form_data.get('product_id'))
    self.supplier_id = int(form_data.get('supplier_id'))