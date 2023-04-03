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