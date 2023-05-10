from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
import requests
import jwt

router = APIRouter()

# Конфигурационные параметры для Google API
GOOGLE_CLIENT_ID = '703772874802-hg25j5apmdseok1d205cnn7c9nemr7ph.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'http://127.0.0.1:8000/api/google_auth/'
GOOGLE_SCOPE = 'profile email'

# Конфигурационные параметры для GitHub API
GITHUB_CLIENT_ID = '87cd4f614d142bd3ad42'
GITHUB_CLIENT_SECRET = '6df189f4f1fcc58e23c94ca62ed7945d0d479ae1'
GITHUB_REDIRECT_URI = 'http://127.0.0.1:8000/api/github_auth/'


def get_access_token_google(code: str) -> str:
  data = {
    "code": code,
    "client_id": GOOGLE_CLIENT_ID,
    "client_secret": GOOGLE_CLIENT_SECRET,
    "redirect_uri": GOOGLE_REDIRECT_URI,
    "grant_type": "authorization_code"
  }
  response = requests.post("https://oauth2.googleapis.com/token", data=data)
  print(response.text)
  return json.loads(response.text).get("access_token")

def get_access_token_github(code: str) -> str:
  data = {
    "code": code,
    "client_id": GITHUB_CLIENT_ID,
    "client_secret": GITHUB_CLIENT_SECRET,
    "redirect_uri": GITHUB_REDIRECT_URI,
  }
  response = requests.post("https://github.com/login/oauth/access_token", data=data)
  response.raise_for_status()
  parsed_response = dict(item.split("=") for item in response.text.split("&"))
  access_token = parsed_response["access_token"]
  return access_token

def get_user_info_google(access_token: str) -> dict:
  headers = {"Authorization": f"Bearer {access_token}"}
  response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
  return json.loads(response.text)

def get_user_info_github(access_token: str) -> dict:
  headers = {"Authorization": f"Bearer {access_token}"}
  response = requests.get("https://api.github.com/user", headers=headers)
  return json.loads(response.text)

jwt_token = ""
secret_key = 'amogus'

@router.get(path='/api/google_auth/', response_class=JSONResponse)
async def google_auth(request: Request):
  code = request.query_params.get("code")
  if not code:
      return {"error": "Authorization code not found"}
  access_token = get_access_token_google(code)
  user_info = get_user_info_google(access_token)  
  payload = {'user_info': user_info}
  global jwt_token
  jwt_token = jwt.encode(payload, secret_key)
  
  return RedirectResponse(url='/', status_code=302)

@router.get(path='/api/github_auth/', response_class=JSONResponse)
async def github_auth(request: Request):
  code = request.query_params.get("code")
  if not code:
      return {"error": "Authorization code not found"}
  access_token = get_access_token_github(code)
  user_info = get_user_info_github(access_token)  
  payload = {'user_info': user_info}
  global jwt_token
  jwt_token = jwt.encode(payload, secret_key)
  
  return RedirectResponse(url='/', status_code=302)

@router.get(path='/api/get_jwt_token/', response_class=JSONResponse)
async def get_jwt_token():
  if (jwt_token == ""):
    return {}
  return {"jwt_token":jwt_token}


security = HTTPBearer()

async def jwt_authentication(credentials: HTTPAuthorizationCredentials = Depends(security)):
  try:
    jwt_token_info = credentials.credentials
    user_data = jwt.decode(jwt_token_info, secret_key, algorithms=['HS256'])
    return user_data

  except jwt.DecodeError:
    raise HTTPException(status_code=401, detail='Invalid JWT token')
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail='Expired JWT token')
  
@router.get(path='/api/get_username/', response_class=JSONResponse)
async def get_username(credentials: HTTPAuthorizationCredentials = Depends(security)):
  try:
    jwt_token_info = credentials.credentials
    user_data = jwt.decode(jwt_token_info, secret_key, algorithms=['HS256'])
    return user_data

  except jwt.DecodeError:
    return {}
  except jwt.ExpiredSignatureError:
    return {}
