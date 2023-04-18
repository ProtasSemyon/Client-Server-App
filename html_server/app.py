from fastapi import FastAPI, Request, responses
import os
import requests

from fastapi.responses import HTMLResponse

import logging

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

@app.get(path='/', response_class=HTMLResponse)
async def route(request: Request):
  with open("./index.html", "r") as f:
    html_content = f.read()
  return HTMLResponse(content=html_content)

@app.get(path='/navigate', response_class=HTMLResponse)
async def navigate(page: str):
  return responses.RedirectResponse(url=page)

@app.get(path='/{path}', response_class=HTMLResponse)
async def get_page(request: Request, path: str):
  print('text')
  response = requests.get('http://' + str(rest_url) + '/' + path)
  return HTMLResponse(content=response.content)
