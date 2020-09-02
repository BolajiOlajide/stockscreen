from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from models import Base


app = FastAPI(
    title="stockscreener",
    description="monitor logs based on yfinance"
)

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def dashboard(request: Request):
    """
    displays the stock screener dashboard / homepage
    """
    context = {"request": request}
    return templates.TemplateResponse("dashboard.html", context)


@app.post("/stock")
def create_stock():
    """
    created a stock and stores it in the database
    """
    return {"code": "success", "message": "stock created"}
