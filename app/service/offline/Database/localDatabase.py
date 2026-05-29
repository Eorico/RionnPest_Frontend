# service/offline/Database/localDatabase.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

_DB_PATH   = Path(__file__).resolve().parent.parent.parent.parent / "local_database.db"

SQLITE_URL = os.getenv("SQLITE_URL", f"sqlite:///{_DB_PATH}")

engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db():
    """
    Create all tables. Import models INSIDE this function (lazy import)
    to break the circular dependency:
      localDatabase → LocalInventory → localDatabase (circular!)
    By importing inside init_db(), the module is fully initialised
    before the import runs.
    """
    from service.offline.Models.LocalInventory import (  # noqa: F401
        LocalAdmin,
        LocalInventory,
        LocalChemicalUsed,
        LocalActualChemicalUsed,
        LocalDocument,
    )
    Base.metadata.create_all(bind=engine)