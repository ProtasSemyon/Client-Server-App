from fastapi import FastAPI, Request, responses
import os
import requests

from fastapi.responses import HTMLResponse, FileResponse
from fastapi.encoders import jsonable_encoder

from fastapi.templating import Jinja2Templates


import logging
import json

templates = Jinja2Templates(directory='./templates')


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='app.log',
    filemode='a'
)

logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

handler2 = logging.FileHandler('app.log')
handler2.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

#logger.addHandler(handler)
logger.addHandler(handler2)

app = FastAPI()

rest_url = os.getenv('REST_SERVER') if os.getenv('REST_SERVER') is not None else '127.0.0.1:8000'

html_template_dict = {
  'customers':'Customers.html',
  'order_items':'OrderItems.html',
  'orders':'Orders.html',
  'products':'Products.html',
  'product_suppliers':'ProductSuppliers.html',
  'suppliers':'Suppliers.html',
}

HTTP = 'http://'

@app.get(path='/', response_class=HTMLResponse)
async def route():
  with open("./index.html", "r") as f:
    html_content = f.read()
  return HTMLResponse(content=html_content)

@app.get(path='/navigate', response_class=HTMLResponse)
async def navigate(page: str):
  return responses.RedirectResponse(url=page)


@app.get(path='/assets/{filename}', response_class=FileResponse)
async def files(filename: str):
  return FileResponse(path='./assets/'+filename)

@app.get(path='/{path}', response_class=HTMLResponse)
async def get_page(request: Request, path: str):
  if path not in html_template_dict.keys():
    return HTMLResponse(status_code=404)
  response = requests.get(HTTP + str(rest_url) + '/' + path)
  json_data = json.loads(jsonable_encoder(response.content))
  json_data.update({"request":request})
  print(json_data)
  return templates.TemplateResponse(html_template_dict[path], json_data)

@app.post(path='/{path}', response_class=HTMLResponse)
async def post_page(request: Request, path: str):
  form = await request.form()
  _id = form.get('id')
  
  match(form.get('_method')):
    case 'PUT':
      response = requests.put(HTTP + str(rest_url) + '/' + path + (('/' + str(_id)) if _id is not None else ''), data=form)
    case 'DELETE':
      response = requests.delete(HTTP + str(rest_url) + '/' + path + '/' + str(_id))
    case _:
      return HTMLResponse(status_code=405)
    
  json_data = json.loads(jsonable_encoder(response.content))
  json_data.update({"request":request})
  return templates.TemplateResponse(html_template_dict[path], json_data)