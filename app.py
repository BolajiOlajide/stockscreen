import yfinance as yf
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Stock

app = FastAPI(title="stockscreener", description="monitor logs based on yfinance")

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


class StockRequest(BaseModel):
    symbol: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def dashboard(request: Request):
    """
    displays the stock screener dashboard / homepage
    """
    context = {"request": request}
    return templates.TemplateResponse("dashboard.html", context)


def fetch_stock_data(id: int):
    db = SessionLocal()
    print("starting background tasks")
    stock = db.query(Stock).filter(Stock.id == id).first()

    # yahoo_data = yf.Ticker(stock.symbol)

    # stock.ma200 = yahoo_data.info["twoHundredDayAverage"]
    # stock.ma50 = yahoo_data.info["fiftyDayAverage"]
    # stock.price = yahoo_data.info["previousClose"]
    # stock.forward_pe = yahoo_data.info["forwardPE"]
    # stock.forward_eps = yahoo_data.info["forwardEps"]
    # stock.dividend_yield = yahoo_data.info["dividendYield"] * 100

    # db.add(stock)
    # db.commit()


# depends as to be the last thing in your controller
@app.post("/stock")
async def create_stock(
    stock_request: StockRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    created a stock and stores it in the database
    """
    stock = Stock(symbol=stock_request.symbol)
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)

    return {"code": "success", "message": "stock created"}
