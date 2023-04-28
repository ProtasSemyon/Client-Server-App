from fastapi import FastAPI, Request, responses, requests
from starlette.datastructures import URL

from fastapi.responses import HTMLResponse, FileResponse

from base import Customers
from base import OrderItems
from base import Orders
from base import Products
from base import Suppliers
from base import ProductSuppliers

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='app.log',
    filemode='a'
)

app = FastAPI()

app.include_router(Customers.router)
app.include_router(Products.router)
app.include_router(Orders.router)
app.include_router(OrderItems.router)
app.include_router(ProductSuppliers.router)
app.include_router(Suppliers.router)


logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

handler2 = logging.FileHandler('app.log')
handler2.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

#logger.addHandler(handler)
logger.addHandler(handler2)

@app.get(path='/', response_class=HTMLResponse)
async def route():
  with open("./app/index.html", "r") as f:
    html_content = f.read()
  return HTMLResponse(content=html_content)

@app.get(path='/app/js/{filename}', response_class=FileResponse)
async def get_file(filename: str):
  return f'./app/js/{filename}'
