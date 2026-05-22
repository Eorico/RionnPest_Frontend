# service/offline/Service/offlineApiService.py
from service.offline.Database.localDatabase import session_local
from service.offline.Repositories.localRepository import (
    local_admin_repo, local_inventory_repo,
)
from service.connections.connectionChecker import is_online


class OfflineCapableApiService:
    """
    Strategy pattern:
      Online  → delegates to real ApiService (MySQL / FastAPI)
      Offline → reads/writes SQLite via local repositories
    """

    def __init__(self, online_api):
        self._api      = online_api
        self._base_url = online_api._base_url
        self._session  = online_api._session
        self.admin_under: str | None = None
        self.auth      = online_api.auth
        self.inventory = online_api.inventory
        self.recycle   = online_api.recycle
        self.documents = online_api.documents

    # ── Connectivity ──────────────────────────────────────────────────────────

    def _online(self) -> bool:
        return is_online(self._base_url)

    def check_connection_service(self) -> bool:
        return self._online()

    # ── Auth ──────────────────────────────────────────────────────────────────

    def login_service(self, username: str, password: str) -> tuple[bool, str]:
        if self._online():
            success, msg = self._api.login_service(username, password)
            if success:
                self.admin_under = username
                self._cache_credentials_after_online_login(username, password)
            return success, msg
        return self._offline_login(username, password)

    def _offline_login(self, username: str, password: str) -> tuple[bool, str]:
        db = session_local()
        try:
            admin = local_admin_repo.verify(db, username, password)
            if admin:
                self.admin_under = username
                return True, "Login Successful (offline)"
            return (False,
                    "Invalid credentials — server unreachable "
                    "and no cached account found")
        finally:
            db.close()

    def _cache_credentials_after_online_login(self, username: str,
                                              plain_password: str):
        """Cache bcrypt hash locally so offline login works next time."""
        from passlib.context import CryptContext
        db = session_local()
        try:
            hashed = CryptContext(
                schemes=["bcrypt"], deprecated="auto").hash(plain_password)
            local_admin_repo.upsert(
                db, username=username, password_hash=hashed,
                role="admin", email=None, offline_registered=False)
        except Exception as e:
            print(f"[OfflineAPI] Could not cache credentials: {e}")
        finally:
            db.close()

    # ── Register ──────────────────────────────────────────────────────────────

    def register_service(self, username: str, password: str,
                         email: str) -> tuple[bool, str]:
        if self._online():
            success, msg = self._api.register_service(username, password, email)
            if success:
                # Also cache locally so the user can log in offline immediately
                db = session_local()
                try:
                    from passlib.context import CryptContext
                    hashed = CryptContext(
                        schemes=["bcrypt"], deprecated="auto").hash(password)
                    local_admin_repo.upsert(
                        db, username=username, password_hash=hashed,
                        role="admin", email=email, offline_registered=False)
                except Exception as e:
                    print(f"[OfflineAPI] Could not cache new admin: {e}")
                finally:
                    db.close()
            return success, msg

        # ── Offline registration ──────────────────────────────────────────────
        return self._offline_register(username, password, email)

    def _offline_register(self, username: str, password: str,
                          email: str) -> tuple[bool, str]:
        """
        Save a new admin account to SQLite only.
        Marked offline_registered=True so SyncManager pushes it to MySQL
        the next time the server is reachable.
        """
        if not username or not password:
            return False, "Username and password are required"

        db = session_local()
        try:
            success, reason = local_admin_repo.register_offline(
                db, username, password, email)
            if success:
                return (True,
                        "Account created locally — "
                        "it will be synced to the server when online")
            return False, reason
        except Exception as e:
            return False, f"Local registration failed: {e}"
        finally:
            db.close()

    # ── Forgot / Reset password ───────────────────────────────────────────────
    # These always require a server connection (OTP sent via Gmail)

    def forgot_password_service(self, username: str) -> tuple[bool, str]:
        if self._online():
            return self._api.forgot_password_service(username)
        return (False,
                "Password reset requires an internet connection — "
                "please connect and try again")

    def reset_password_service(self, username: str, otp: str,
                               new_password: str) -> tuple[bool, str]:
        if self._online():
            return self._api.reset_password_service(username, otp, new_password)
        return (False,
                "Password reset requires an internet connection — "
                "please connect and try again")

    def logout_service(self):
        self._api.logout_service()
        self.admin_under = None

    # ── Inventory ─────────────────────────────────────────────────────────────

    def get_active_inventory(self) -> list:
        if self._online():
            return self._api.get_active_inventory()
        return self._offline_get_inventory()

    def _offline_get_inventory(self) -> list:
        db = session_local()
        try:
            result = []
            for r in local_inventory_repo.get_all(db):
                result.append({
                    "id":             r.id,
                    "admin_under":    r.admin_under,
                    "category":       r.category,
                    "client_name":    r.client_name,
                    "date":           r.date,
                    "month":          r.month,
                    "year":           r.year,
                    "start_time":     r.start_time,
                    "end_time":       r.end_time,
                    "start_meridiem": r.start_meridiem,
                    "end_meridiem":   r.end_meridiem,
                    "chemicals_use": [
                        {"chemical_name": c.chemical_name,
                         "quantity": c.quantity, "remarks": c.remarks}
                        for c in r.chemicals_use
                    ],
                    "actual_chemicals_used": [
                        {"actual_chemicals_name": c.actual_chemicals_name,
                         "quantity": c.quantity, "remarks": c.remarks}
                        for c in r.actual_chemicals_used
                    ],
                    "_offline": True,
                })
            return result
        finally:
            db.close()

    def add_inventory_record(self, data: dict) -> tuple[bool, str]:
        if self._online():
            return self._api.add_inventory_record(data)
        db = session_local()
        try:
            local_inventory_repo.save(db, data)
            return True, "Saved locally — will sync when back online"
        except Exception as e:
            return False, f"Local save failed: {e}"
        finally:
            db.close()

    def update_inventory_record(self, record_id, data) -> tuple[bool, str]:
        if self._online():
            return self._api.update_inventory_record(record_id, data)
        return False, "Cannot update records while offline"

    # ── Recycle bin, Documents — online only ──────────────────────────────────

    def get_recycle_bin(self) -> list:
        return self._api.get_recycle_bin() if self._online() else []

    def move_to_bin(self, record_id) -> tuple[bool, str]:
        return self._api.move_to_bin(record_id) if self._online() \
               else (False, "Cannot trash records while offline")

    def restore_record(self, record_id) -> tuple[bool, str]:
        return self._api.restore_record(record_id) if self._online() \
               else (False, "Cannot restore records while offline")

    def restore_all(self) -> tuple[bool, str]:
        return self._api.restore_all() if self._online() \
               else (False, "Cannot restore records while offline")

    def permanent_delete(self, record_id) -> tuple[bool, str]:
        return self._api.permanent_delete(record_id) if self._online() \
               else (False, "Cannot permanently delete while offline")

    def upload_document(self, title, file_name, file_data) -> tuple[bool, str]:
        return self._api.upload_document(title, file_name, file_data) if self._online() \
               else (False, "Cannot upload documents while offline")

    def get_documents(self) -> list:
        return self._api.get_documents() if self._online() else []

    def download_document(self, doc_id) -> bytes | None:
        return self._api.download_document(doc_id) if self._online() else None

    def delete_document(self, doc_id) -> tuple[bool, str]:
        return self._api.delete_document(doc_id) if self._online() \
               else (False, "Cannot delete documents while offline")