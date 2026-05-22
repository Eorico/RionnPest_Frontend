# service/offline/Repositories/localRepository.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from service.offline.Models.LocalInventory import (
    LocalAdmin, LocalInventory,
    LocalChemicalUsed, LocalActualChemicalUsed,
)

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LocalAdminRepository:

    def upsert(self, db: Session, username: str, password_hash: str,
               role: str, email: str | None,
               offline_registered: bool = False) -> LocalAdmin:
        """Insert or update a cached admin row."""
        admin = db.query(LocalAdmin).filter_by(username=username).first()
        if admin:
            admin.password_hash      = password_hash
            admin.role               = role
            admin.email              = email
            # Don't overwrite offline_registered if already True
            if offline_registered:
                admin.offline_registered = True
        else:
            admin = LocalAdmin(
                username=username,
                password_hash=password_hash,
                role=role,
                email=email,
                offline_registered=offline_registered,
            )
            db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin

    def register_offline(self, db: Session, username: str,
                         plain_password: str, email: str,
                         role: str = "admin") -> tuple[bool, str]:
        """
        Create a brand-new admin account locally while offline.
        Returns (True, "") on success or (False, reason) on failure.
        """
        # Check for duplicate username locally
        if db.query(LocalAdmin).filter_by(username=username).first():
            return False, "Username already exists locally"

        # Check for duplicate email locally
        if email and db.query(LocalAdmin).filter_by(email=email).first():
            return False, "Email already registered locally"

        hashed = _pwd.hash(plain_password)
        admin  = LocalAdmin(
            username=username,
            password_hash=hashed,
            role=role,
            email=email,
            offline_registered=True,   # must be synced to MySQL later
        )
        db.add(admin)
        db.commit()
        return True, ""

    def get_pending_registrations(self, db: Session) -> list[LocalAdmin]:
        """Return all admins registered offline that haven't been pushed to MySQL."""
        return db.query(LocalAdmin).filter_by(offline_registered=True).all()

    def mark_synced_registration(self, db: Session, username: str):
        admin = db.query(LocalAdmin).filter_by(username=username).first()
        if admin:
            admin.offline_registered = False
            db.commit()

    def verify(self, db: Session, username: str,
               plain_password: str) -> LocalAdmin | None:
        """Verify credentials against cached bcrypt hash."""
        admin = db.query(LocalAdmin).filter_by(username=username).first()
        if not admin:
            return None
        try:
            if _pwd.verify(plain_password, admin.password_hash):
                return admin
        except Exception:
            pass
        return None


class LocalInventoryRepository:

    def save(self, db: Session, data: dict) -> LocalInventory:
        record = LocalInventory(
            admin_under    = data.get("admin_under"),
            category       = data.get("category", "treatment"),
            client_name    = data.get("client_name"),
            date           = data.get("date"),
            month          = data.get("month"),
            year           = data.get("year"),
            start_time     = data.get("start_time"),
            end_time       = data.get("end_time"),
            start_meridiem = data.get("start_meridiem"),
            end_meridiem   = data.get("end_meridiem"),
            synced         = False,
        )
        db.add(record)
        db.flush()

        for c in data.get("chemical_use", []):
            db.add(LocalChemicalUsed(
                inventory_id  = record.id,
                chemical_name = c.get("chemical_name", ""),
                quantity      = c.get("quantity", ""),
                remarks       = c.get("remarks", ""),
            ))

        for c in data.get("actual_chemical_used", []):
            db.add(LocalActualChemicalUsed(
                inventory_id          = record.id,
                actual_chemicals_name = c.get("chemical_name", ""),
                quantity              = c.get("quantity", ""),
                remarks               = c.get("remarks", ""),
            ))

        db.commit()
        db.refresh(record)
        return record

    def get_all(self, db: Session) -> list[LocalInventory]:
        return db.query(LocalInventory).all()

    def get_unsynced(self, db: Session) -> list[LocalInventory]:
        return db.query(LocalInventory).filter_by(synced=False).all()

    def mark_synced(self, db: Session, record_id: int):
        r = db.query(LocalInventory).filter_by(id=record_id).first()
        if r:
            r.synced = True
            db.commit()

    def delete(self, db: Session, record_id: int):
        r = db.query(LocalInventory).filter_by(id=record_id).first()
        if r:
            db.delete(r)
            db.commit()


local_admin_repo     = LocalAdminRepository()
local_inventory_repo = LocalInventoryRepository()