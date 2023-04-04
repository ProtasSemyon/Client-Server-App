from typing import Optional
from sqlmodel import Field, SQLModel

class SuppliersModel(SQLModel):
  supplier_id : Optional[int] = Field(default=None, primary_key=True)
  supplier_name : str
  contact_name : str
  email : str
  phone : str
  
  
class Suppliers(SuppliersModel, table=True):
  __tablename__ : str = 'suppliers'
  
  def __init__(self, form_data):
    self.set_value_from_form(form_data)
  
  def set_value_from_form(self, form_data):
    self.supplier_name = str(form_data.get('supplier_name'))
    self.contact_name = str(form_data.get('contact_name'))
    self.email = str(form_data.get('email'))
    self.phone = str(form_data.get('phone'))