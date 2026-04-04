import requests

def is_online():
    try:
        requests.get("", timeout=2)
        return True
    except:
        pass