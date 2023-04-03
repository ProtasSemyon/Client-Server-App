from typing import Optional
from sqlmodel import Field, SQLModel

class CustomersModel(SQLModel):
  customer_id :Optional[int] = Field(default=None, primary_key=True)
  first_name :str
  last_name :str
  email :str = Field(unique=True)
  phone :str
  
class Customers(CustomersModel, table=True):
  __tablename__ : str = 'customers'
  
  def __init__(self, form_data):
    self.set_value_from_form(form_data)
  
  def set_value_from_form(self, form_data):
    self.first_name = str(form_data.get('first_name'))
    self.last_name = str(form_data.get('last_name'))
    self.email = str(form_data.get('email'))
    self.phone = str(form_data.get('phone'))

  
