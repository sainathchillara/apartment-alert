from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db
from .utils import send_alert_email

router = APIRouter()

@router.post("/alerts/", response_model=schemas.Alert)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    new_alert = crud.create_alert(db=db, alert=alert)
    send_alert_email(alert.email, alert.dict())  # send the email
    return new_alert

@router.get("/alerts/", response_model=list[schemas.Alert])
def read_alerts(
    skip: int = 0,
    limit: int = 100,
    min_price: int = 0,
    max_price: int = 0,
    bedrooms: int = 0,
    bathrooms: int = 0,
    db: Session = Depends(get_db)
):
    return crud.get_filtered_alerts(
        db=db,
        skip=skip,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        bathrooms=bathrooms
    )

@router.get("/alerts/{email}", response_model=list[schemas.Alert])
def get_alerts_by_email(email: str, db: Session = Depends(get_db)):
    return crud.get_alerts_by_email(db, email)

@router.delete("/alerts/{alert_id}", response_model=schemas.Alert)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    return crud.delete_alert(db, alert_id)
