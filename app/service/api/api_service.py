from dotenv import load_dotenv
import os, requests

load_dotenv()

class ApiService:
    def __init__(self):
        self.base_url = str(os.getenv("API_SERVICE", "http://127.0.0.1:8000"))
        self.session = requests.Session()
        
    def check_connection_service(self):
        try:
            response = self.session.get(f"{self.base_url}/inventory/", timeout=2) 
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
        
    def login_service(self, username, password):
        try:
            payload = {"username": username, "password": password}
            response = self.session.post(f"{self.base_url}/auth/login", json=payload, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if token: 
                    self.session.headers.update({"Authorization": f"Bearer {token}"})
                return True, "Login Successful"
            return False, "Invalid Credentials"
        except requests.exceptions.RequestException as e:
            return False, f"Server Error: {str(e)}"
        
    def logout_service(self):
        self.session.headers.pop("Authorization", None)
        
    def get_active_inventory(self):
        try:
            response = self.session.get(f"{self.base_url}/inventory/")
            return response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return []
        
    def get_recycle_bin(self):
        try:
            response = self.session.get(f"{self.base_url}/inventory/recycle-bin")
            return response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return []
        
    def add_inventory_record(self, data):
        try:
            response = self.session.post(f"{self.base_url}/inventory/", json=data, timeout=5)
            return response.status_code == 200, response.text
        except requests.exceptions.RequestException as e:
            return False, str(e)
        
    def move_to_bin(self, record_id):
        try:
            response = self.session.delete(f"{self.base_url}/inventory/{record_id}")
            if response.status_code == 200:
                return True, response.json().get("message", "Moved to bin")
            return False, f"Server Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e)
        
    def restore_record(self, record_id):
        try:
            response = self.session.post(f"{self.base_url}/inventory/restore/{record_id}")
            if response.status_code == 200:
                return True, response.json().get("message", "Record restored")
            return False, f"Server Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e) 
        
    def restore_all(self):
        try:
            response = self.session.post(f"{self.base_url}/inventory/restore-all")
            if response.status_code == 200:
                return True, response.json().get("message", "All record restored")
            return False, f"Server Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e)
        
    def permanent_delete(self, record_id):
        try:
            response = self.session.delete(f"{self.base_url}/inventory/permanent/{record_id}")
            if response.status_code == 200:
                return True, response.json().get("message", "Permanently deleted")
            return False, f"Server Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e)