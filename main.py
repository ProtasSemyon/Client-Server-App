from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from typing import List
from sqlmodel import Session, select # type: ignore

from server.db_connect import get_session
from server.app import app