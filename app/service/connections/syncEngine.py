import os
import requests
from dotenv import load_dotenv
from service.offline.Database.localDatabase import session_local
from service.offline.Models.LocalInventory import LocalInventory

load_dotenv()

class SyncManager:
    def __init__(self, api_service):
        self.api = api_service
        self.endpoint = f"{self.api}/inventory/"

    def is_online(self):
        """Check connection to the specific backend server."""
        try:
            # We ping the base URL to see if the server is alive
            requests.get(self.api, timeout=2)
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
                    "chemical_name": record.chemicals_use,
                    "actual_chemical_on_hand": record.actual_chemicals_used
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