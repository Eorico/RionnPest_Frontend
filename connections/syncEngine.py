from offline.Database.localDatabase import SessionLocal
from offline.Models.LocalInventory import LocalInventory
from connectionChecker import is_online
import requests

def sync_data():
    if not is_online():
        return
    
    db = SessionLocal()
    
    unsynced = db.query(LocalInventory).filter_by(synced=False).all()
    
    for record in unsynced:
        data = {
            "treatmentDate": str(record.treatmentDate),
            "clientName": record.clientName,
            "startTime": str(record.startTime),
            "endTime": str(record.endTime),
            "chemicalName": record.chemicalName,
            "actualChemicalOnHand": record.actualChemicalOnHand
        }
        
        try:
            response = requests.post(
                "", json=data
            )
            
            if response.status_code == 200:
                record.synced = True
                db.commit()
            
        except:
            continue
        
    db.close()