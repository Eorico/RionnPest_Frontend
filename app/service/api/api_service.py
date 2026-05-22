from dotenv import load_dotenv
import os, requests

from .auth_api_service import AuthApiService
from .inventory_api_service import InventoryApiService
from .recycle_api_service import RecycleBinApiService
from .document_service import DocumentApiService
from .base import IConnectionService
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class ApiService(IConnectionService):
    def __init__(self):
        self._base_url = str(os.getenv("API_SERVICE", "http://127.0.0.1:8000"))
        self._session = requests.Session()
        self.admin_under: str | None = None
        
        self.auth = AuthApiService(self._base_url, self._session)
        self.inventory = InventoryApiService(self._base_url, self._session)
        self.recycle = RecycleBinApiService(self._base_url, self._session)
        self.documents = DocumentApiService(self._base_url, self._session)
        
    def check_connection_service(self) -> bool:
        try:
            r = self._session.get(f"{self._base_url}/inventory/", timeout=2)
            return r.status_code == 200
        except requests.exceptions.RequestException:
            return False
        
    def login_service(self, username, password):
        return self.auth.login_service(username, password)
 
    def register_service(self, username, password, email):
        return self.auth.register_service(username, password, email)
 
    def forgot_password_service(self, username):
        return self.auth.forgot_password_service(username)
 
    def reset_password_service(self, username, otp, new_password):
        return self.auth.reset_password_service(username, otp, new_password)
 
    def logout_service(self):
        self.auth.logout_service()
 
    def get_active_inventory(self):
        return self.inventory.get_active_inventory()
 
    def add_inventory_record(self, data):
        return self.inventory.add_inventory_record(data)
 
    def update_inventory_record(self, record_id, data):
        return self.inventory.update_inventory_record(record_id, data)
 
    def get_recycle_bin(self):
        return self.recycle.get_recycle_bin()
 
    def move_to_bin(self, record_id):
        return self.recycle.move_to_bin(record_id)
 
    def restore_record(self, record_id):
        return self.recycle.restore_record(record_id)
 
    def restore_all(self):
        return self.recycle.restore_all()
 
    def permanent_delete(self, record_id):
        return self.recycle.permanent_delete(record_id)
 
    def upload_document(self, title, file_name, file_data):
        return self.documents.upload_document(title, file_name, file_data)
 
    def get_documents(self):
        return self.documents.get_documents()
 
    def download_document(self, doc_id):
        return self.documents.download_document(doc_id)
 
    def delete_document(self, doc_id):
        return self.documents.delete_document(doc_id)
     