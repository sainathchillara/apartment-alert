from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session

from . import models, crud
from .alerts import router as alert_router
from .database import get_db
from .schemas import AlertCreate

app = FastAPI()
app.include_router(alert_router)

templates = Jinja2Templates(directory="app/templates")


# ✅ Root route to prevent 404 on home
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/html-alerts", response_class=HTMLResponse)
def html_alerts(
    request: Request,
    email: str = "",
    location: str = "",
    message: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(models.Alert)
    if email:
        query = query.filter(models.Alert.email.ilike(f"%{email}%"))
    if location:
        query = query.filter(models.Alert.location.ilike(f"%{location}%"))
    alerts = query.order_by(models.Alert.created_at.desc()).all()
    return templates.TemplateResponse("alerts.html", {
        "request": request,
        "alerts": alerts,
        "email": email,
        "location": location,
        "message": message
    })


@app.post("/create-alert")
def create_alert_form(
    email: str = Form(...),
    location: str = Form(...),
    min_price: int = Form(0),
    max_price: int = Form(0),
    bedrooms: int = Form(0),
    bathrooms: int = Form(0),
    db: Session = Depends(get_db)
):
    existing = db.query(models.Alert).filter_by(
        email=email,
        location=location,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        bathrooms=bathrooms
    ).first()
    if not existing:
        alert_data = AlertCreate(
            email=email,
            location=location,
            min_price=min_price,
            max_price=max_price,
            bedrooms=bedrooms,
            bathrooms=bathrooms
        )
        crud.create_alert(db=db, alert=alert_data)
        return RedirectResponse(url="/html-alerts?message=Alert+created!", status_code=HTTP_303_SEE_OTHER)
    return RedirectResponse(url="/html-alerts?message=Alert+already+exists", status_code=HTTP_303_SEE_OTHER)


@app.post("/delete-alert")
def delete_alert_form(alert_id: int = Form(...), db: Session = Depends(get_db)):
    crud.delete_alert(db, alert_id)
    return RedirectResponse(url="/html-alerts?message=Alert+deleted!", status_code=HTTP_303_SEE_OTHER)


@app.post("/edit-alert")
def edit_alert_form(
    alert_id: int = Form(...),
    email: str = Form(...),
    location: str = Form(...),
    min_price: int = Form(0),
    max_price: int = Form(0),
    bedrooms: int = Form(0),
    bathrooms: int = Form(0),
    db: Session = Depends(get_db)
):
    crud.update_alert(db, alert_id, {
        "email": email,
        "location": location,
        "min_price": min_price,
        "max_price": max_price,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms
    })
    return RedirectResponse(url="/html-alerts?message=Alert+updated!", status_code=HTTP_303_SEE_OTHER)
