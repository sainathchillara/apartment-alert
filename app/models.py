from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    location = Column(String)
    min_price = Column(Integer)
    max_price = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 