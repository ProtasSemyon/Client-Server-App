from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select # type: ignore
from fastapi import FastAPI, Request, Depends, responses
from fastapi.responses import HTMLResponse
from server.db_connect import get_session

from server.base.Customers import Customers
from server.base.OrderItems import OrderItems
from server.base.Orders import Orders
from server.base.Products import Products


templates = Jinja2Templates(directory='server/templates')
app = FastAPI()


@app.get(path='/', response_class=HTMLResponse)
async def route(request: Request):
  with open("server/index.html", "r") as f:
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
      error_message = e.args
  elif action =='/add':
    customer = Customers(first_name=str(form_data.get('first_name')), 
                         last_name=str(form_data.get('last_name')), 
                         email=str(form_data.get('email')), 
                         phone=str(form_data.get('phone')))
    db.add(customer)
    db.commit()
  elif action == '/update':
    statement = select(Customers).where(Customers.customer_id == key)
    customer = db.exec(statement).one()
    customer.first_name = str(form_data.get('first_name'))
    customer.last_name = str(form_data.get('last_name'))
    customer.email = str(form_data.get('email'))
    customer.phone = str(form_data.get('phone'))
    
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
