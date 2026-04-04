from sqlalchemy import (
    Column, Integer, String, Float, Date,
    Time, Boolean
)
from service.offline.Database.localDatabase import Base

class LocalInventory(Base):
    __tablename__ = "inventory_records"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    category = Column(String(20), default="treatment")
    client_name = Column(String(100))
    start_time = Column(Time)
    end_time = Column(Time)
    chemical_name = Column(String(100))
    actual_chemical_on_hand = Column(Float)
    
    synced = Column(Boolean, default=False)