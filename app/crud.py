from sqlalchemy.orm import Session
from . import models, schemas
from .utils import send_alert_email


def get_existing_alert(db: Session, alert: schemas.AlertCreate):
    return db.query(models.Alert).filter_by(
        email=alert.email,
        location=alert.location,
        min_price=alert.min_price,
        max_price=alert.max_price,
        bedrooms=alert.bedrooms,
        bathrooms=alert.bathrooms,
    ).first()


def create_alert(db: Session, alert: schemas.AlertCreate):
    existing = get_existing_alert(db, alert)
    if existing:
        return None  # Prevent duplicate

    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)

    # Send email only after creation
    send_alert_email(db_alert.email, alert.dict())

    return db_alert


def get_alerts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Alert).offset(skip).limit(limit).all()


def get_alerts_by_email(db: Session, email: str):
    return db.query(models.Alert).filter(models.Alert.email == email).all()


def delete_alert(db: Session, alert_id: int):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if alert:
        db.delete(alert)
        db.commit()
    return alert


def get_filtered_alerts(
    db: Session,
    skip: int,
    limit: int,
    min_price: int,
    max_price: int,
    bedrooms: int,
    bathrooms: int
):
    query = db.query(models.Alert)

    if min_price > 0:
        query = query.filter(models.Alert.min_price >= min_price)
    if max_price > 0:
        query = query.filter(models.Alert.max_price <= max_price)
    if bedrooms > 0:
        query = query.filter(models.Alert.bedrooms >= bedrooms)
    if bathrooms > 0:
        query = query.filter(models.Alert.bathrooms >= bathrooms)

    return query.offset(skip).limit(limit).all()
