# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    email: str
    location: str
    min_price: int
    max_price: int
    bedrooms: int
    bathrooms: int

class AlertCreate(BaseModel):
    email: str
    location: str
    min_price: int = 0
    max_price: int = 0
    bedrooms: int = 0
    bathrooms: int = 0

class Alert(AlertBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows ORM to model conversion
