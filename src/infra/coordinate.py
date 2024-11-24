import requests
from decimal import Decimal

def get_coordinate(address: str) -> dict:
    headers = {
        "User-Agent": "LLocalFastAi/1.0"
    }
    try:
        response = requests.get(
            f"https://nominatim.openstreetmap.org/search?limit=1&format=json&q={address}",
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            return {
                "latitude": Decimal(0.0), 
                "longitude": Decimal(0.0)
            }
        return {
            "latitude": Decimal(data[0]["lat"]),
            "longitude": Decimal(data[0]["lon"])
        }
    except (requests.RequestException, KeyError, IndexError):
        return {
            "latitude": Decimal(0.0), 
            "longitude": Decimal(0.0)
        }
