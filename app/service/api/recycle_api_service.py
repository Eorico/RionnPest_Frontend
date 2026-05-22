# service/api/recycle_bin_service.py
from .base import BaseApiService, IRecycleBinService


class RecycleBinApiService(BaseApiService, IRecycleBinService):

    def get_recycle_bin(self) -> list:
        try:
            r = self._session.get(f"{self._base_url}/inventory/recycle-bin")
            return r.json() if r.status_code == 200 else []
        except Exception:
            return []

    def move_to_bin(self, record_id: int) -> tuple[bool, str]:
        try:
            r = self._session.delete(f"{self._base_url}/inventory/{record_id}")
            if r.status_code == 200:
                return True, r.json().get("message", "Moved to bin")
            return False, f"Server Error: {r.status_code}"
        except Exception as e:
            return False, str(e)

    def restore_record(self, record_id: int) -> tuple[bool, str]:
        try:
            r = self._session.post(
                f"{self._base_url}/inventory/restore/{record_id}")
            if r.status_code == 200:
                return True, r.json().get("message", "Record restored")
            return False, f"Server Error: {r.status_code}"
        except Exception as e:
            return False, str(e)

    def restore_all(self) -> tuple[bool, str]:
        try:
            r = self._session.post(
                f"{self._base_url}/inventory/restore-all")
            if r.status_code == 200:
                return True, r.json().get("message", "All records restored")
            return False, f"Server Error: {r.status_code}"
        except Exception as e:
            return False, str(e)

    def permanent_delete(self, record_id: int) -> tuple[bool, str]:
        try:
            r = self._session.delete(
                f"{self._base_url}/inventory/permanent/{record_id}")
            if r.status_code == 200:
                return True, r.json().get("message", "Permanently deleted")
            return False, f"Server Error: {r.status_code}"
        except Exception as e:
            return False, str(e)