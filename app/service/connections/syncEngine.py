# service/connections/syncEngine.py
import requests
from service.offline.Database.localDatabase import session_local
from service.offline.Repositories.localRepository import (
    local_admin_repo, local_inventory_repo,
)
from service.connections.connectionChecker import is_online


class SyncManager:

    def __init__(self, api_service):
        self.api       = api_service
        self._base_url = api_service._base_url

    def check_online(self) -> bool:
        return is_online(self._base_url)

    # ── alias so intro.py calling sync_data() still works ────────────────────
    def sync_data(self) -> tuple[bool, str]:
        """Alias for sync_pending_records — keeps intro.py compatible."""
        return self.sync_pending_records()

    def sync_pending_records(self) -> tuple[bool, str]:
        if not self.check_online():
            return False, "Server unreachable — will retry when online"

        db = session_local()
        try:
            pending = local_inventory_repo.get_unsynced(db)
            if not pending:
                return True, "Nothing to sync"

            synced_count = 0
            failed       = []

            for record in pending:
                payload = {
                    "admin_under":    record.admin_under,
                    "category":       record.category,
                    "client_name":    record.client_name,
                    "date":           record.date,
                    "month":          record.month,
                    "year":           record.year,
                    "start_time":     record.start_time,
                    "end_time":       record.end_time,
                    "start_meridiem": record.start_meridiem,
                    "end_meridiem":   record.end_meridiem,
                    "chemical_use": [
                        {
                            "chemical_name": c.chemical_name,
                            "quantity":      c.quantity,
                            "remarks":       c.remarks,
                        }
                        for c in record.chemicals_use
                    ],
                    "actual_chemical_used": [
                        {
                            "chemical_name": c.actual_chemicals_name,
                            "quantity":      c.quantity,
                            "remarks":       c.remarks,
                        }
                        for c in record.actual_chemicals_used
                    ],
                }
                try:
                    resp = requests.post(
                        f"{self._base_url}/inventory/",
                        json=payload, timeout=5,
                        headers=self.api._session.headers,
                    )
                    if resp.status_code == 200:
                        local_inventory_repo.mark_synced(db, record.id)
                        synced_count += 1
                    else:
                        failed.append(record.id)
                except Exception as e:
                    failed.append(record.id)
                    print(f"[SyncManager] Failed record {record.id}: {e}")

            msg = f"Synced {synced_count}/{len(pending)} records"
            if failed:
                msg += f" | Failed: {failed}"
            return True, msg

        except Exception as e:
            return False, str(e)
        finally:
            db.close()

    def cache_admin_credentials(self, username: str,
                                password_hash: str,
                                role: str, email: str | None):
        db = session_local()
        try:
            local_admin_repo.upsert(db, username, password_hash, role, email)
        finally:
            db.close()