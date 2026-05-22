# service/api/document_service.py
from .base import BaseApiService, IDocumentService


class DocumentApiService(BaseApiService, IDocumentService):

    def upload_document(self, title: str, file_name: str,
                        file_data: bytes) -> tuple[bool, str]:
        try:
            r = self._session.post(
                f"{self._base_url}/documents/",
                data={"title": title, "file_name": file_name},
                files={"file": (file_name, file_data)},
                timeout=10,
            )
            if r.status_code == 200:
                return True, r.json()
            return False, r.text
        except Exception as e:
            return False, str(e)

    def get_documents(self) -> list:
        try:
            r = self._session.get(f"{self._base_url}/documents/")
            return r.json() if r.status_code == 200 else []
        except Exception:
            return []

    def download_document(self, doc_id: int) -> bytes | None:
        try:
            r = self._session.get(
                f"{self._base_url}/documents/{doc_id}/download", timeout=10)
            return r.content if r.status_code == 200 else None
        except Exception:
            return None

    def delete_document(self, doc_id: int) -> tuple[bool, str]:
        try:
            r = self._session.delete(f"{self._base_url}/documents/{doc_id}")
            if r.status_code == 200:
                return True, r.json().get("message", "Deleted")
            return False, f"Server Error: {r.status_code}"
        except Exception as e:
            return False, str(e)