from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select # type: ignore
from fastapi import FastAPI, Request, Depends, responses
from fastapi.responses import HTMLResponse
from db_connect import get_session

from base.Customers import Customers
from base.OrderItems import OrderItems
from base.Orders import Orders
from base.Products import Products
from base.Suppliers import Suppliers
from base.ProductSuppliers import ProductSuppliers

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='app.log',
    filemode='a'
)

ERROR_MESSAGE = "You can't delete this row: it has connections with other tables"

templates = Jinja2Templates(directory='./templates')
app = FastAPI()

logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

handler2 = logging.FileHandler('app.log')
handler2.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

#logger.addHandler(handler)
logger.addHandler(handler2)



@app.get(path='/', response_class=HTMLResponse)
async def route(request: Request):
  with open("./index.html", "r") as f:
    html_content = f.read()
  return HTMLResponse(content=html_content)

@app.get(path='/navigate', response_class=HTMLResponse)
async def navigate(page: str):
  return responses.RedirectResponse(url=page)

@app.get(path='/customers', response_class=HTMLResponse)
async def get_customers(request: Request, db: Session = Depends(get_session)):
  smth = select(Customers)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Customers.html", {"request":request,"customers":result})

@app.post(path='/customers', response_class=HTMLResponse)
async def update_customers(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(Customers).where(Customers.customer_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError as e:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    customer = Customers(form_data)
    db.add(customer)
    db.commit()
  elif action == '/update':
    statement = select(Customers).where(Customers.customer_id == key)
    customer = db.exec(statement).one()
    customer.set_value_from_form(form_data)
    
    db.add(customer)
    db.commit()
    
  smth = select(Customers)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Customers.html", {"request":request,"customers":result, "error_message":error_message})

@app.get(path='/products', response_class=HTMLResponse)
async def get_products(request: Request, db: Session = Depends(get_session)):
  smth = select(Products)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Products.html", {"request":request,"products":result})

@app.post(path='/products', response_class=HTMLResponse)
async def update_products(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(Products).where(Products.product_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError as e:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    products = Products(form_data)
    db.add(products)
    db.commit()
  elif action == '/update':
    statement = select(Products).where(Products.product_id == key)
    products = db.exec(statement).one()
    products.set_value_from_form(form_data)
    
    db.add(products)
    db.commit()
    
  smth = select(Products)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Products.html", {"request":request,"products":result, "error_message":error_message})

@app.get(path='/suppliers', response_class=HTMLResponse)
async def get_suppliers(request: Request, db: Session = Depends(get_session)):
  smth = select(Suppliers)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Suppliers.html", {"request":request,"suppliers":result})

@app.post(path='/suppliers', response_class=HTMLResponse)
async def update_suppliers(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(Suppliers).where(Suppliers.supplier_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError as e:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    supplier = Suppliers(form_data)
    db.add(supplier)
    db.commit()
  elif action == '/update':
    statement = select(Suppliers).where(Suppliers.supplier_id == key)
    supplier = db.exec(statement).one()
    supplier.set_value_from_form(form_data)
    
    db.add(supplier)
    db.commit()
    
  smth = select(Suppliers)
  result = db.exec(smth).all()
  return templates.TemplateResponse("Suppliers.html", {"request":request,"suppliers":result, "error_message":error_message})

@app.get(path='/product_suppliers', response_class=HTMLResponse)
async def get_product_suppliers(request: Request, db: Session = Depends(get_session)):
  smth = select(ProductSuppliers, Products, Suppliers).join(Products).join(Suppliers)
  products_st = select(Products)
  suppliers_st = select(Suppliers)
  result = db.exec(smth).all()
  products = db.exec(products_st).all()
  suppliers = db.exec(suppliers_st).all()
  return templates.TemplateResponse("ProductSuppliers.html", {"request":request,"product_suppliers":result, "products":products, "suppliers":suppliers})

@app.post(path='/product_suppliers', response_class=HTMLResponse)
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
    
  smth = select(ProductSuppliers, Products, Suppliers).join(Products).join(Suppliers)
  products_st = select(Products)
  suppliers_st = select(Suppliers)
  result = db.exec(smth).all()
  products = db.exec(products_st).all()
  suppliers = db.exec(suppliers_st).all()
  return templates.TemplateResponse("ProductSuppliers.html", {"request":request,"product_suppliers":result, "products":products, "suppliers":suppliers, "error_message":error_message})

@app.get(path='/orders', response_class=HTMLResponse)
async def get_orders(request: Request, db: Session = Depends(get_session)):
  smth = select(Orders, Customers).join(Customers)
  result = db.exec(smth).all()
  customers = db.exec(select(Customers)).all()
  return templates.TemplateResponse("Orders.html", {"request":request,"orders":result, "customers":customers})

@app.post(path='/orders', response_class=HTMLResponse)
async def update_orders(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(Orders).where(Orders.order_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    order = Orders(form_data)
    db.add(order)
    db.commit()
  elif action == '/update':
    statement = select(Orders).where(Orders.order_id == key)
    order = db.exec(statement).one()
    order.set_value_from_form(form_data) # type: ignore
    db.add(order)
    db.commit()
    
  smth = select(Orders, Customers).join(Customers)
  result = db.exec(smth).all()
  customers = db.exec(select(Customers)).all()
  return templates.TemplateResponse("Orders.html", {"request":request,"orders":result, "customers":customers, "error_message":error_message})
    
@app.get(path='/order_items', response_class=HTMLResponse)
async def get_order_items(request: Request, db: Session = Depends(get_session)):
  smth = select(OrderItems, Orders, Products).join(Orders).join(Products)
  result = db.exec(smth).all()
  products = db.exec(select(Products)).all()
  orders = db.exec(select(Orders)).all()

  return templates.TemplateResponse("OrderItems.html", {"request":request,"order_items":result, "products":products, "orders":orders})

@app.post(path='/order_items', response_class=HTMLResponse)
async def update_order_items(request: Request, db: Session = Depends(get_session)):
  error_message = ""
  form_data = await request.form()
  action = form_data.get('action')
  key = form_data.get('id')
  if action == '/delete':
    statement = select(OrderItems).where(OrderItems.order_item_id == key)
    result = db.exec(statement).one()
    try:
      db.delete(result)
      db.commit()
    except IntegrityError:
      db.rollback()
      error_message = ERROR_MESSAGE
  elif action =='/add':
    order_items = OrderItems(form_data)
    db.add(order_items)
    db.commit()
  elif action == '/update':
    statement = select(OrderItems).where(OrderItems.order_item_id == key)
    order_items = db.exec(statement).one()
    order_items.set_value_from_form(form_data)
    db.add(order_items)
    db.commit()
    
  smth = select(OrderItems, Orders, Products).join(Orders).join(Products)
  result = db.exec(smth).all()
  products = db.exec(select(Products)).all()
  orders = db.exec(select(Orders)).all()

  return templates.TemplateResponse("OrderItems.html", {"request":request,"order_items":result, "products":products, "orders":orders})
  