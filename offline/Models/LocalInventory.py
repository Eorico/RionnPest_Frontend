from sqlalchemy import (
    Column, Integer, String, Float, Date,
    Time, Boolean
)
from datetime import date

class LocalInventory:
    __tablename__ = "inventory_records"
    
    id = Column(Integer, primary_key=True, index=True)
    treatmentDate = Column(Date)
    clientName = Column(String(100))
    startTime = Column(Time)
    endTime = Column(Time)
    chemicalName = Column(String(100))
    actualChemicalOnHand = Column(Float)
    
    synced = Column(Boolean, default=False)