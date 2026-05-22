import requests

def is_online(base_url: str, timeout: int = 2) -> bool:
    try:
        requests.get(f"{base_url}/inventory/", timeout=timeout)
        return True
    except:
        return False