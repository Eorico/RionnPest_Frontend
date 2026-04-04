import os
import requests
from dotenv import load_dotenv
from service.offline.Database.localDatabase import session_local
from service.offline.Models.LocalInventory import LocalInventory

load_dotenv()

class SyncManager:
    def __init__(self):
        self.api_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
        self.endpoint = f"{self.api_url}/inventory/"

    def is_online(self):
        """Check connection to the specific backend server."""
        try:
            # We ping the base URL to see if the server is alive
            requests.get(self.api_url, timeout=2)
            return True
        except:
            return False

    def sync_data(self):
        """Pushes local unsynced records to the cloud MySQL database."""
        if not self.is_online():
            return False, "Still Offline"

        db = session_local()
        try:
            unsynced = db.query(LocalInventory).filter_by(synced=False).all()
            
            if not unsynced:
                return True, "Already Synced"

            for record in unsynced:
                data = {
                    "Date": str(record.date),
                    "client_name": record.client_name,
                    "start_time": str(record.start_time),
                    "end_time": str(record.end_time),
                    "chemical_name": record.chemical_name,
                    "actual_chemical_on_hand": record.actual_chemical_on_hand
                }

                response = requests.post(self.endpoint, json=data)
                
                if response.status_code == 200:
                    record.synced = True
                    db.commit()
            
            return True, f"Synced {len(unsynced)} records"
        except Exception as e:
            return False, str(e)
        finally:
            db.close()