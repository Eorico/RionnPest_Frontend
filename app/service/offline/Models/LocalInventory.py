from sqlalchemy import (
    Column, Integer, String, Float, Date,
    Time, Boolean, ForeignKey
)
from service.offline.Database.localDatabase import Base
from sqlalchemy.orm import relationship

class LocalInventory(Base):
    __tablename__ = "inventory_records"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    category = Column(String(20), default="treatment")
    client_name = Column(String(100))
    start_time = Column(Time)
    end_time = Column(Time)
    
    chemicals_use = relationship("LocalChemicalUsed", back_populates="parent_record", cascade="all, delete-orphan")
    actual_chemicals_used = relationship("LocalActualChemicalUsed", back_populates="parent_record", cascade="all, delete-orphan")
    
    synced = Column(Boolean, default=False)
    
class LocalChemicalUsed(Base):
    __tablename__ = "local_chemicals_used"
    
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("local_inventory_records.id"))
    chemical_name = Column(String(100))
    quantity = Column(Float)
    
    parent_record = relationship("LocalInventory", back_populates="chemicals_used")

class LocalActualChemicalUsed(Base):
    __tablename__ = "local_actual_chemicals_used"
    
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("local_inventory_records.id"))
    actual_chemical_name = Column(String(100))
    quantity = Column(Float)
    
    parent_record = relationship("LocalInventory", back_populates="actual_chemicals_used")