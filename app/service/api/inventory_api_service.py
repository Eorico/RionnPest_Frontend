# service/api/inventory_service.py
from .base import BaseApiService, IInventoryService

class InventoryApiService(BaseApiService, IInventoryService):

    def get_active_inventory(self) -> list:
        try:
            r = self._session.get(f"{self._base_url}/inventory/")
            return r.json() if r.status_code == 200 else []
        except Exception:
            return []

    def add_inventory_record(self, data: dict) -> tuple[bool, str]:
        try:
            r = self._session.post(
                f"{self._base_url}/inventory/", json=data, timeout=5)
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)

    def update_inventory_record(self, record_id: int,
                                data: dict) -> tuple[bool, str]:
        try:
            payload = {
                "date":           data.get("date"),
                "month":          data.get("month"),
                "year":           data.get("year"),
                "category":       data.get("category"),
                "client_name":    data.get("client_name"),
                "start_time":     data.get("start_time"),
                "end_time":       data.get("end_time"),
                "start_meridiem": data.get("start_meridiem"),
                "end_meridiem":   data.get("end_meridiem"),
                "chemicals_use": [
                    {
                        "chemical_name": c.get("chemical_name") or c.get("name") or "",
                        "quantity":      c.get("quantity") or c.get("qty") or "",
                        "remarks":       c.get("remarks") or "",
                    }
                    for c in data.get("chemicals_use", data.get("chemical_use", []))
                ],
                "actual_chemicals_used": [
                    {
                        "actual_chemicals_name": (
                            c.get("actual_chemicals_name")
                            or c.get("chemical_name")
                            or c.get("name") or ""
                        ),
                        "quantity": c.get("quantity") or c.get("qty") or "",
                        "remarks":  c.get("remarks") or "",
                    }
                    for c in data.get(
                        "actual_chemicals_used",
                        data.get("actual_chemical_used", []))
                ],
            }
            r = self._session.patch(
                f"{self._base_url}/inventory/{record_id}",
                json=payload, timeout=5,
            )
            if r.status_code == 200:
                return True, r.json()
            return False, f"Server Error {r.status_code}: {r.text}"
        except Exception as e:
            return False, str(e)