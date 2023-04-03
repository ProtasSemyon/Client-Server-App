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

  
