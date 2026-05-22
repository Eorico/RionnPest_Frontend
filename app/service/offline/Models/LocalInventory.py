# service/offline/Models/LocalInventory.py
from sqlalchemy import (
    Column, Integer, String, Float,
    Boolean, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from service.offline.Database.localDatabase import Base


class LocalAdmin(Base):
    """Cached admin credentials for offline login."""
    __tablename__ = "local_admins"

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    username           = Column(String(50),  unique=True, nullable=False)
    password_hash      = Column(String(555), nullable=False)
    role               = Column(String(50),  default="admin")
    email              = Column(String(255), nullable=True)
    offline_registered = Column(Boolean,     default=False)  # ← ADD THIS LINE

class LocalInventory(Base):
    """One treatment / inspection record saved locally while offline."""
    __tablename__ = "local_inventory_records"   # ← fixed table name

    id          = Column(Integer, primary_key=True, autoincrement=True)
    admin_under = Column(String(50),  nullable=True)
    category    = Column(String(20),  default="treatment")
    client_name = Column(String(100), nullable=True)
    date        = Column(Integer,     nullable=True)   # day
    month       = Column(Integer,     nullable=True)
    year        = Column(Integer,     nullable=True)
    start_time  = Column(String(20),  nullable=True)
    end_time    = Column(String(20),  nullable=True)
    start_meridiem = Column(String(5), nullable=True)
    end_meridiem   = Column(String(5), nullable=True)
    synced      = Column(Boolean,     default=False)
    created_at  = Column(DateTime,    nullable=True)

    chemicals_use = relationship(
        "LocalChemicalUsed",
        back_populates="parent_record",
        cascade="all, delete-orphan",
    )
    actual_chemicals_used = relationship(
        "LocalActualChemicalUsed",
        back_populates="parent_record",
        cascade="all, delete-orphan",
    )


class LocalChemicalUsed(Base):
    __tablename__ = "local_chemicals_used"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    inventory_id = Column(Integer, ForeignKey("local_inventory_records.id"))  # ← fixed
    chemical_name = Column(String(100), nullable=True)
    quantity     = Column(String(50),  nullable=True)   # string to match API
    remarks      = Column(String(255), nullable=True)

    parent_record = relationship("LocalInventory", back_populates="chemicals_use")


class LocalActualChemicalUsed(Base):
    __tablename__ = "local_actual_chemicals_used"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    inventory_id = Column(Integer, ForeignKey("local_inventory_records.id"))  # ← fixed
    actual_chemicals_name = Column(String(100), nullable=True)
    quantity     = Column(String(50),  nullable=True)
    remarks      = Column(String(255), nullable=True)

    parent_record = relationship(
        "LocalInventory", back_populates="actual_chemicals_used")