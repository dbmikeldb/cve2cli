# app/services/psirt.py

import httpx

from urllib.parse import urlencode
from typing import Optional

from backend.app.core.config import settings

client_id = settings.cisco_client_id
client_secret = settings.cisco_client_secret


AUTH_URL = "https://id.cisco.com/oauth2/default/v1/token"
PSIRT_API_URL = "https://api.cisco.com/security/advisories/cve/"


async def get_access_token() -> str:
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(AUTH_URL,
                                data=urlencode(data),
                                headers=headers)
        resp.raise_for_status()

        return resp.json()["access_token"]
    

async def fetch_cve_data(cve_id: str) -> Optional[dict]:
    token = await get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PSIRT_API_URL}{cve_id}",
                                headers=headers)
        
        if resp.status_code == 200:
            return resp.json()
        
        elif resp.status_code == 404:
            return None
        
        else:
            resp.raise_for_status()
