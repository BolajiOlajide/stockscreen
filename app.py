from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def dashboard(request: Request):
    """
    displays the stock screener dashboard / homepage
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("dashboard.html", context)


@app.post("/stock")
def create_stock():
    """
    created a stock and stores it in the database
    """
    return {
        "code": "success",
        "message": "stock created"
    }
