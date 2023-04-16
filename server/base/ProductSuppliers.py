from typing import Optional
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends, responses
from fastapi.responses import HTMLResponse
from db_connect import get_session
templates = Jinja2Templates(directory='./templates')
ERROR_MESSAGE = "You can't delete this row: it has connections with other tables"

from sqlmodel import Field, SQLModel
from base import Suppliers
from base import Products

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
    
router = APIRouter()

@router.get(path='/product_suppliers', response_class=HTMLResponse)
async def get_product_suppliers(request: Request, db: Session = Depends(get_session)):
  smth = select(ProductSuppliers, Products.Products, Suppliers.Suppliers).join(Products.Products).join(Suppliers.Suppliers)
  products_st = select(Products.Products)
  suppliers_st = select(Suppliers.Suppliers)
  result = db.exec(smth).all()
  products = db.exec(products_st).all()
  suppliers = db.exec(suppliers_st).all()
  return templates.TemplateResponse("ProductSuppliers.html", {"request":request,"product_suppliers":result, "products":products, "suppliers":suppliers})

@router.post(path='/product_suppliers', response_class=HTMLResponse)
async def update_product_suppliers(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(ProductSuppliers).where(ProductSuppliers.product_supplier_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError as e:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    product_supplier = ProductSuppliers(form_data)
    db.add(product_supplier)
    db.commit()
  elif action == '/update':
    statement = select(ProductSuppliers).where(ProductSuppliers.product_supplier_id == key)
    product_supplier = db.exec(statement).one()
    product_supplier.set_value_from_form(form_data)
    
    db.add(product_supplier)
    db.commit()
    
  smth = select(ProductSuppliers, Products.Products, Suppliers.Suppliers).join(Products.Products).join(Suppliers.Suppliers)
  products_st = select(Products.Products)
  suppliers_st = select(Suppliers.Suppliers)
  result = db.exec(smth).all()
  products = db.exec(products_st).all()
  suppliers = db.exec(suppliers_st).all()
  return templates.TemplateResponse("ProductSuppliers.html", {"request":request,"product_suppliers":result, "products":products, "suppliers":suppliers, "error_message":error_message})