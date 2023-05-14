from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select # type: ignore
from fastapi import APIRouter, Request, Depends, responses
from fastapi.responses import JSONResponse

from db_connect import get_session
import json
from login import jwt_authentication

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

@router.get(path='/api/product_suppliers', response_class=JSONResponse)
async def get_product_suppliers(db: Session = Depends(get_session)):
  smth = select(ProductSuppliers, Products.Products, Suppliers.Suppliers).join(Products.Products).join(Suppliers.Suppliers)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  suppliers = db.exec(select(Suppliers.Suppliers)).all()
  return {"product_suppliers":result, "products":products, "suppliers":suppliers}

@router.delete(path='/api/product_suppliers/{p_s_id}', response_class=JSONResponse, dependencies=[Depends(jwt_authentication)])
async def delete_product_suppliers(p_s_id: int, db: Session = Depends(get_session)):
  error = ""
  statement = select(ProductSuppliers).where(ProductSuppliers.product_supplier_id == p_s_id) # type: ignore
  result = db.exec(statement).one()
  try:
    db.delete(result)
    db.commit()
  except IntegrityError as e:
    db.rollback()
    error = ERROR_MESSAGE
    
  smth = select(ProductSuppliers, Products.Products, Suppliers.Suppliers).join(Products.Products).join(Suppliers.Suppliers)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  suppliers = db.exec(select(Suppliers.Suppliers)).all()
  return {"product_suppliers":result, "products":products, "suppliers":suppliers, "error_message":error}

@router.put(path='/api/product_suppliers/{p_s_id}', response_class=JSONResponse, dependencies=[Depends(jwt_authentication)])
async def update_product_suppliers(request: Request, p_s_id: int, db: Session = Depends(get_session)):
  form_data = json.loads(await request.body())
  statement = select(ProductSuppliers).where(ProductSuppliers.product_supplier_id == p_s_id) # type: ignore
  product_supplier = db.exec(statement).one()
  product_supplier.set_value_from_form(form_data)
  
  db.add(product_supplier)
  db.commit()
  
  smth = select(ProductSuppliers, Products.Products, Suppliers.Suppliers).join(Products.Products).join(Suppliers.Suppliers)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  suppliers = db.exec(select(Suppliers.Suppliers)).all()
  return {"product_suppliers":result, "products":products, "suppliers":suppliers}

@router.put(path='/api/product_suppliers', response_class=JSONResponse, dependencies=[Depends(jwt_authentication)])
async def add_product_suppliers(request: Request, db: Session = Depends(get_session)):
  form_data = json.loads(await request.body())

  product_supplier = ProductSuppliers(form_data)
  db.add(product_supplier)
  db.commit()
    
  smth = select(ProductSuppliers, Products.Products, Suppliers.Suppliers).join(Products.Products).join(Suppliers.Suppliers)
  result = db.exec(smth).all()
  products = db.exec(select(Products.Products)).all()
  suppliers = db.exec(select(Suppliers.Suppliers)).all()
  return {"product_suppliers":result, "products":products, "suppliers":suppliers}